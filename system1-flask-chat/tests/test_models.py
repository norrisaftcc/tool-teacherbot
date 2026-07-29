import pytest
from models import (
    DEFAULT_TOKEN_BUDGET, _FALLBACK_TOKEN_BUDGET, _budget_from_env,
    Group, Conversation, Message,
)


# ---- GROUP_TOKEN_BUDGET parsing -------------------------------------------
#
# Parsed at import, so a bad value takes the app down before any request.
# The error has to name the variable — a bare ValueError from mid-import
# tells an operator nothing about which env var to fix.

@pytest.mark.parametrize('raw', [None, '', '   '])
def test_budget_falls_back_when_unset(raw):
    assert _budget_from_env(raw) == _FALLBACK_TOKEN_BUDGET


def test_budget_accepts_a_valid_override():
    assert _budget_from_env('5000000') == 5_000_000


@pytest.mark.parametrize('raw', ['lots', '25_000_000x', '1e6', '3.5'])
def test_budget_rejects_non_integers_by_name(raw):
    with pytest.raises(RuntimeError) as excinfo:
        _budget_from_env(raw)
    assert 'GROUP_TOKEN_BUDGET' in str(excinfo.value)


@pytest.mark.parametrize('raw', ['0', '-1'])
def test_budget_rejects_zero_and_negative(raw):
    """A budget of zero locks out the cohort on their first message, and the
    service looks perfectly healthy while doing it."""
    with pytest.raises(RuntimeError) as excinfo:
        _budget_from_env(raw)
    assert 'positive' in str(excinfo.value)

def test_group_defaults(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='group1', clearance_level='ORANGE')
        db.session.add(g)
        db.session.commit()
        assert g.token_budget == DEFAULT_TOKEN_BUDGET
        assert g.tokens_used == 0


def test_default_budget_survives_the_most_expensive_module(app):
    """The budget must outlast a class period, not a handful of messages.

    csc134's m4 window composes to ~27.5k tokens, and every message pays it
    because `_usage_total` counts cache reads at full weight. The old
    100_000 default bought fewer than four messages for an entire cohort.
    """
    worst_case_prompt_tokens = 27_500
    students, messages_each = 25, 30
    assert DEFAULT_TOKEN_BUDGET >= worst_case_prompt_tokens * students * messages_each

def test_conversation_linked_to_group(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='group2', clearance_level='YELLOW')
        db.session.add(g)
        db.session.commit()
        c = Conversation(group_id=g.id)
        db.session.add(c)
        db.session.commit()
        assert c.group_id == g.id

def test_message_linked_to_conversation(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='group3', clearance_level='ORANGE')
        db.session.add(g)
        db.session.commit()
        c = Conversation(group_id=g.id)
        db.session.add(c)
        db.session.commit()
        m = Message(conversation_id=c.id, role='user', content='Hello', tokens_used=5)
        db.session.add(m)
        db.session.commit()
        assert m.role == 'user'
        assert m.tokens_used == 5

def test_group_increment_tokens(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='group4', clearance_level='ORANGE')
        db.session.add(g)
        db.session.commit()
        g.increment_tokens(500)
        db.session.commit()
        assert g.tokens_used == 500
        assert g.tokens_remaining == DEFAULT_TOKEN_BUDGET - 500

# ---- budget backfill ------------------------------------------------------
#
# A column default only applies on INSERT and there is no migrations
# framework, so rows already in production keep the budget they were created
# with. Without this, raising the default fixes new cohorts only.

def test_raise_budget_floor_lifts_a_stale_row(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='stale', clearance_level='ORANGE', token_budget=100_000)
        db.session.add(g)
        db.session.commit()

        assert g.raise_budget_floor() is True
        assert g.token_budget == DEFAULT_TOKEN_BUDGET


def test_raise_budget_floor_never_lowers_a_deliberate_cap(app):
    """Raise-only. An instructor's lower cap must not be silently undone."""
    with app.app_context():
        from models import db
        db.create_all()
        capped = DEFAULT_TOKEN_BUDGET * 2
        g = Group(name='generous', clearance_level='ORANGE', token_budget=capped)
        db.session.add(g)
        db.session.commit()

        assert g.raise_budget_floor() is False
        assert g.token_budget == capped


def test_group_tokens_cannot_exceed_budget(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='group5', clearance_level='ORANGE', token_budget=100)
        db.session.add(g)
        db.session.commit()
        g.increment_tokens(150)  # exceeds budget
        db.session.commit()
        assert g.tokens_used == 100      # clamped at budget
        assert g.tokens_remaining == 0   # never goes negative
