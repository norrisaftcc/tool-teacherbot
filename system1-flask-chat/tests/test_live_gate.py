"""The gate deciding whether live tests skip or must run.

Deliberately NOT marked `live` — this runs in the ordinary offline suite,
because the failure it guards against is a live job reporting green without
making a single API call, and a guard that only runs under the condition it
guards is not a guard.
"""
import pytest

from live_gate import KEY_VAR, REQUIRE_VAR, has_key, live_required, should_skip


# ---- has_key --------------------------------------------------------------
#
# An unset GitHub Actions secret expands to '' rather than leaving the
# variable undefined, so presence-in-environ is not the question.

@pytest.mark.parametrize('value', ['', '   ', '\n'])
def test_blank_key_is_not_a_key(value):
    assert has_key({KEY_VAR: value}) is False


def test_absent_key_is_not_a_key():
    assert has_key({}) is False


def test_real_key_is_a_key():
    assert has_key({KEY_VAR: 'sk-ant-whatever'}) is True


# ---- the decision ---------------------------------------------------------

def test_skips_locally_without_a_key():
    """A contributor running `-m live` with no key gets a reason, not a fail."""
    assert should_skip({}) is True


def test_does_not_skip_when_a_key_is_present():
    assert should_skip({KEY_VAR: 'sk-ant-x'}) is False


def test_ci_without_a_key_must_not_skip():
    """The whole point.

    If the repo secret is missing or misnamed, `secrets.ANTHROPIC_API_KEY`
    expands to '' and every live test would skip — leaving a green job that
    made no API calls, which is indistinguishable from a passing one.
    """
    assert should_skip({REQUIRE_VAR: '1'}) is False


def test_ci_with_a_key_does_not_skip():
    assert should_skip({REQUIRE_VAR: '1', KEY_VAR: 'sk-ant-x'}) is False


@pytest.mark.parametrize('value', ['0', 'true', 'yes', '', 'TRUE'])
def test_require_is_exactly_one_and_nothing_else(value):
    """Strict, so a typo in the workflow fails open to skipping rather than
    silently half-enabling the guard."""
    assert live_required({REQUIRE_VAR: value}) is False


def test_require_accepts_one_with_whitespace():
    assert live_required({REQUIRE_VAR: ' 1 '}) is True
