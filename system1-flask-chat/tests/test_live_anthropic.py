"""Tests that call the real Anthropic API.

Deselected by default — `pytest.ini` sets `-m "not live"`, so the ordinary
suite stays offline and free. Opt in with `pytest -m live`, and give it a
key. CI runs these from .github/workflows/live.yml on manual dispatch plus
a weekly schedule, never on pull requests: fork PRs cannot read secrets and
would fail confusingly, and it would spend on every push.

**What belongs here, and what does not.** These assert *mechanics* — that
caching engages, that the composed prompt is accepted, that token
accounting matches what the SDK returns. They do not assert that the bot
behaved well; K3 is frozen on that ("eval flags are triage, never a
verdict"), so persona judgement stays in evals/ and reports rather than
gates. See K16.
"""
import os

import pytest

from live_gate import MISSING_KEY_IN_CI, has_key, live_required, should_skip

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(
        # Skip, not fail: a contributor running `-m live` without a key
        # should get a clear reason, not an auth traceback. CI sets
        # REQUIRE_LIVE_TESTS=1, which removes that grace — see live_gate.
        should_skip(),
        reason=f'{"ANTHROPIC_API_KEY"} not set',
    ),
]


@pytest.fixture(autouse=True)
def _fail_rather_than_skip_in_ci():
    """A green run that made no API calls is the failure mode to prevent.

    Reached only when REQUIRE_LIVE_TESTS=1 suppressed the skipif above; with
    no key the tests would otherwise raise an opaque auth error, which reads
    as a broken test rather than a broken workflow.
    """
    if live_required() and not has_key():
        pytest.fail(MISSING_KEY_IN_CI)

SKIN = 'csc134'
MODULE = 'm0'


@pytest.fixture(scope='module')
def composed():
    """The real composed prompt for csc134/m0, exactly as routes.py builds it.

    Pinned to m0 explicitly rather than trusting the registry default, so a
    CSC134_ACTIVE_MODULE set on the runner cannot silently change what these
    tests measure.
    """
    import auth
    import claude_handler

    # Restored on teardown. monkeypatch is function-scoped and this fixture
    # is module-scoped, so the save/restore is manual — leaving the override
    # set would make any later test that reads CSC134_ACTIVE_MODULE depend on
    # whether this module ran first.
    var = f'{SKIN.upper()}_ACTIVE_MODULE'
    previous = os.environ.get(var)
    os.environ[var] = MODULE
    try:
        context = auth.load_skin_context(SKIN)
        persona = auth.load_skin_persona(SKIN)
        notes = auth.load_skin_notes(SKIN)
        yield {
            'blocks': claude_handler._system_blocks(context, persona, notes),
            'context': context,
            'persona': persona,
            'notes': notes,
            'model': auth.SKINS[SKIN]['model'],
        }
    finally:
        if previous is None:
            os.environ.pop(var, None)
        else:
            os.environ[var] = previous


def _call(composed, message):
    """One turn against the real API, returning the raw response.

    Goes through `_system_blocks` — the same cached-block construction the
    chat endpoints use — rather than a hand-built system prompt, because the
    cache_control on that block is the thing under test.
    """
    from claude_handler import client
    return client.messages.create(
        model=composed['model'],
        max_tokens=64,
        system=composed['blocks'],
        messages=[{'role': 'user', 'content': message}],
    )


def test_prompt_caching_actually_engages(composed):
    """The real version of test_auth.py's cache-floor guard.

    `test_every_csc134_module_window_clears_the_haiku_cache_floor` asserts a
    *character-count estimate* clears 4096 tokens, because Haiku declines to
    cache a shorter prefix silently — no error, no warning, just an uncached
    prompt billed at full rate on every message. That test is a proxy. This
    one measures the thing itself.

    Asserted on the second call, not the first: the block carries a 1h TTL,
    so a run within an hour of a previous one sees a cache *read* where a
    cold run sees a cache *write*. Requiring cache_creation on call one
    would go red for the least interesting possible reason.
    """
    first = _call(composed, 'how do i open my codespace')
    second = _call(composed, 'what is cout')

    warmed = (getattr(first.usage, 'cache_creation_input_tokens', 0) or 0) \
        + (getattr(first.usage, 'cache_read_input_tokens', 0) or 0)
    assert warmed > 0, (
        'The first call neither wrote nor read a cache entry. Haiku refuses '
        'to cache a prefix under 4096 tokens and says nothing about it, so '
        'the likely cause is a corpus trim that took the m0 window under the '
        f'floor. usage={first.usage!r}'
    )

    cache_read = getattr(second.usage, 'cache_read_input_tokens', 0) or 0
    assert cache_read > 0, (
        'The second call did not read the cached prefix. Note the two calls '
        'send *different* user messages on purpose — what is cached is the '
        'system block (persona + notes + windowed corpus), not the turn. A '
        'miss here means the prefix is not byte-stable between requests, not '
        f'that the questions differed. usage={second.usage!r}'
    )

    # The point of ADR-0002 is that the corpus stops being fresh input on
    # every message. If the window were being re-sent, input_tokens would
    # dwarf the cached read rather than the other way round.
    assert second.usage.input_tokens < cache_read, (
        f'The corpus looks like it is still being sent fresh: '
        f'input_tokens={second.usage.input_tokens} vs '
        f'cache_read_input_tokens={cache_read}'
    )


def test_composed_prompt_round_trips(composed):
    """Smoke: the real prompt, the real model, through the real entry point.

    Catches a model id that no longer exists, a revoked key, a window grown
    past the context limit, and a malformed cache_control block — none of
    which any mocked test can see.
    """
    from claude_handler import get_claude_response

    text, tokens = get_claude_response(
        composed['context'], [], 'what is this course about',
        model=composed['model'],
        persona=composed['persona'],
        notes=composed['notes'],
    )

    assert text.strip(), 'empty response body'
    assert tokens > 0, '_usage_total reported no tokens for a real call'


def test_usage_total_counts_every_field_the_sdk_returns(composed):
    """Guards the budget against an SDK field rename.

    `_usage_total` sums four named attributes with `getattr(..., 0)`
    fallbacks, so a renamed or added billing field would be silently counted
    as zero — the budget would drift low and nothing would fail. Compare
    against the usage object the API actually returned.
    """
    from claude_handler import _USAGE_FIELDS, _usage_total

    response = _call(composed, 'hello')
    usage = response.usage

    expected = sum(
        value for value in (getattr(usage, f, 0) for f in _USAGE_FIELDS)
        if isinstance(value, int)
    )
    assert _usage_total(usage) == expected

    # Every field _usage_total names must still exist on the response, or it
    # is silently contributing zero.
    missing = [f for f in _USAGE_FIELDS if not hasattr(usage, f)]
    assert not missing, (
        f'_USAGE_FIELDS names attributes the SDK no longer returns: {missing}. '
        f'They are being counted as zero. usage={usage!r}'
    )
