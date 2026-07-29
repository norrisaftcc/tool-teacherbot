import os
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# The old default was 100_000, set on 2026-05-12 — before ADR-0002 (07-25)
# made every message carry the windowed corpus as a cached system prefix.
# `claude_handler._usage_total` counts `cache_read_input_tokens` at full
# weight (correct as a token count; it is not a cost proxy, since cache
# reads bill at roughly a tenth of list), so the prefix is charged against
# this budget on *every* message, cached or not.
#
# Measured composed prompts for csc134, by active module:
#   m0 ~6.3k est / ~7.2k actual   m3,m5,m6,m7 ~5.1-5.7k
#   m1,m2 ~17.3-17.8k             m4 ~24.2k est / ~27.5k actual
#
# So 100_000 was ~13 messages for an entire cohort during m0, and fewer
# than 4 during m4 — shared across every student in the skin. The first
# class period would have ended the cohort, with routes.py telling everyone
# "Token budget exhausted. Contact your instructor." and no admin UI to
# raise it.
#
# 25M sizes the worst module for a real section: 25 students x ~36 messages
# x ~27.5k = ~24.75M. This is a stopgap and the unit is still wrong — the
# budget belongs on a seat, not a cohort, so one verbose student cannot
# lock out the class. That is ADR-0004's call.
_FALLBACK_TOKEN_BUDGET = 25_000_000


def _budget_from_env(raw: str | None) -> int:
    """Parse GROUP_TOKEN_BUDGET, or fail with something an operator can act on.

    This runs at import, so a bad value takes the whole app down before a
    single request. `int()` alone raises a bare ValueError from the middle of
    a module import — in Render's logs that is a stack trace with no mention
    of which variable is wrong, on a service that was working an hour ago.

    Zero and negatives are rejected rather than accepted: a budget of 0 makes
    `tokens_remaining <= 0` true immediately, so every student in the cohort
    is told "Token budget exhausted. Contact your instructor." and the
    instructor finds a healthy service serving a locked-out class. Refusing
    to boot is the better failure, same reasoning as app._require_secrets.
    """
    if raw is None or raw.strip() == '':
        return _FALLBACK_TOKEN_BUDGET

    try:
        value = int(raw)
    except ValueError:
        raise RuntimeError(
            f'GROUP_TOKEN_BUDGET must be an integer number of tokens, '
            f'got {raw!r}. Unset it to use the default '
            f'({_FALLBACK_TOKEN_BUDGET:,}).'
        ) from None

    if value <= 0:
        raise RuntimeError(
            f'GROUP_TOKEN_BUDGET must be positive, got {value}. A budget of '
            f'zero or less locks out every student in the cohort on their '
            f'first message.'
        )
    return value


DEFAULT_TOKEN_BUDGET = _budget_from_env(os.getenv('GROUP_TOKEN_BUDGET'))


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    clearance_level = db.Column(db.String(20), nullable=False)
    token_budget = db.Column(db.Integer, default=lambda: DEFAULT_TOKEN_BUDGET,
                             nullable=False)
    tokens_used = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    conversations = db.relationship('Conversation', backref='group', lazy=True)

    @property
    def tokens_remaining(self):
        return self.token_budget - self.tokens_used

    def increment_tokens(self, count):
        self.tokens_used = min(self.tokens_used + count, self.token_budget)

    def raise_budget_floor(self) -> bool:
        """Lift a stale budget up to the current default. Returns True if changed.

        A column default only applies on INSERT, and there is no migrations
        framework (`db.create_all()` creates missing tables and nothing
        else), so the Group rows already in production keep the 100_000 that
        was written when they were created. Raising the default alone would
        fix new cohorts and leave the live ones at ~4 messages.

        Raise-only, never lower: this must not quietly undo a deliberate cap.
        Nothing can have set one yet — there is no UI or route to edit a
        budget — but that will not stay true.

        Remove this when the budget moves to a per-seat unit (ADR-0004);
        it exists only to carry existing rows across that gap.
        """
        if self.token_budget < DEFAULT_TOKEN_BUDGET:
            self.token_budget = DEFAULT_TOKEN_BUDGET
            return True
        return False


class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    messages = db.relationship('Message', backref='conversation', lazy=True)


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tokens_used = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
