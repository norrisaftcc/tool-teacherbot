"""Decide whether live tests skip or must run.

Not a test module. It exists as its own file so the decision is a pure
function that the *offline* suite can test — the whole point is that this
logic must not be able to fail silently, and logic living inside a
`live`-marked module would itself be deselected by default.

The problem it solves: the live tests skip when `ANTHROPIC_API_KEY` is
absent, which is right for a developer running `pytest -m live` with no key
and wrong for CI. If the repository secret is missing, misnamed, or not
visible to the workflow, `secrets.ANTHROPIC_API_KEY` expands to an empty
string, every live test skips, and the job goes **green having tested
nothing**. A skipped test and a passing test are the same colour.

So CI sets `REQUIRE_LIVE_TESTS=1`, which turns "no key" from a skip into a
failure.
"""
from __future__ import annotations

import os

KEY_VAR = 'ANTHROPIC_API_KEY'
REQUIRE_VAR = 'REQUIRE_LIVE_TESTS'

MISSING_KEY_IN_CI = (
    f'{REQUIRE_VAR}=1 but {KEY_VAR} is empty. The workflow secret is missing, '
    f'misnamed, or not exposed to this job. Failing rather than skipping: '
    f'these tests would otherwise report green having made no API calls.'
)


def has_key(env: dict[str, str] | None = None) -> bool:
    """True when a non-blank API key is present.

    Blank-not-absent is the case that matters: an unset GitHub secret
    expands to `''` rather than leaving the variable undefined, so
    `'ANTHROPIC_API_KEY' in os.environ` is True and useless.
    """
    env = os.environ if env is None else env
    return bool((env.get(KEY_VAR) or '').strip())


def live_required(env: dict[str, str] | None = None) -> bool:
    """True when a missing key must fail instead of skip. CI sets this."""
    env = os.environ if env is None else env
    return (env.get(REQUIRE_VAR) or '').strip() == '1'


def should_skip(env: dict[str, str] | None = None) -> bool:
    """Skip only when there is no key *and* nobody insisted the tests run."""
    return not has_key(env) and not live_required(env)
