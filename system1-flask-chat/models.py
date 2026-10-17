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

# Group.token_budget is db.Integer, which is int4 on Postgres. A larger value
# is accepted by SQLite (the test database) and rejected by Postgres at the
# first INSERT, so a bad per-skin budget would pass every test and then 500
# the first login in production. Refusing at import is the better failure.
MAX_TOKEN_BUDGET = 2**31 - 1


def validate_skin_budget(name: str, value) -> int:
    """Check a per-skin token budget, or fail naming ``name``.

    ``name`` is the env var (or skin key) an operator would edit. The range
    is 0 < value < 2**31 - 1: positive for the reason ``_budget_from_env``
    gives, and strictly below the int4 maximum so ``tokens_used + count``
    arithmetic done in SQL-adjacent code never reaches the column limit.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise RuntimeError(f'{name} must be an integer number of tokens, got {value!r}.')
    if value <= 0:
        raise RuntimeError(
            f'{name} must be positive, got {value}. A budget of zero or less '
            f'locks out every student in the skin on their first message.'
        )
    if value >= MAX_TOKEN_BUDGET:
        raise RuntimeError(
            f'{name} must be below {MAX_TOKEN_BUDGET:,} (the largest value '
            f'the integer budget column holds on Postgres), got {value:,}.'
        )
    return value


def skin_budget_from_env(name: str, default: int) -> int:
    """Read a per-skin budget from the environment, validated.

    Unset or blank means ``default``. A non-integer value raises with the
    variable name, because ``int()`` alone fails from the middle of the
    auth import with a bare ValueError that names nothing.
    """
    raw = os.getenv(name)
    if raw is None or raw.strip() == '':
        return validate_skin_budget(name, default)
    try:
        value = int(raw)
    except ValueError:
        raise RuntimeError(
            f'{name} must be an integer number of tokens, got {raw!r}. '
            f'Unset it to use the default ({default:,}).'
        ) from None
    return validate_skin_budget(name, value)


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

    def raise_budget_floor(self, floor: int | None = None) -> bool:
        """Lift a stale budget up to ``floor``. Returns True if changed.

        A column default only applies on INSERT, so the Group rows already in
        production keep the 100_000 that was written when they were created.
        Raising the default alone would fix new cohorts and leave the live
        ones at ~4 messages.

        This was originally justified by there being no migrations framework.
        ADR-0006 falsified that — a data migration could do this now. The
        method stays because it is already written and already tested, not
        because the alternative is unavailable.

        ``floor`` defaults to the global ``DEFAULT_TOKEN_BUDGET``. A skin that
        declares its own ``token_budget`` passes it here: the global default
        is the wrong floor for that skin, because a skin budget below it would
        be silently raised back to 25M on every login, defeating the cap.

        Raise-only, never lower: this must not quietly undo a deliberate cap.
        Nothing can have set one yet — there is no UI or route to edit a
        budget — but that will not stay true.

        Remove this when the budget moves to a per-seat unit (ADR-0004);
        it exists only to carry existing rows across that gap.
        """
        if floor is None:
            floor = DEFAULT_TOKEN_BUDGET
        if self.token_budget < floor:
            self.token_budget = floor
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
