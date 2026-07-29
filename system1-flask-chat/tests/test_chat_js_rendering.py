"""Runs the JavaScript render check, if node is available.

The rendering path is the one piece of security-relevant logic in this repo
that Python cannot reach: `marked.parse()` output goes to `innerHTML`, and
marked has not sanitized since v5. A Python test can assert the source
*looks* right; only running it proves it.

The npm dependency is gone. `render_check.mjs` now evaluates the vendored
`static/js/marked.umd.js` — the bytes the browser actually executes — rather
than importing the npm ESM build, so the check needs nothing installed and
`node` is the only requirement. That also removed a skip condition that had
become a liability: it gated a security test on `node_modules/marked`
existing, and a skipped test reads exactly like a passing one.
"""
import shutil
import subprocess
from pathlib import Path

import pytest

CHECK = Path(__file__).resolve().parent / 'js' / 'render_check.mjs'
REPO_ROOT = Path(__file__).resolve().parents[2]
VENDORED_MARKED = REPO_ROOT / 'system1-flask-chat' / 'static' / 'js' / 'marked.umd.js'


def test_marked_is_vendored():
    """No skip on this one.

    If the vendored bundle goes missing, the render check below would skip or
    error for an unrelated-looking reason, and chat.html would 404 its only
    script. Fail plainly instead.
    """
    assert VENDORED_MARKED.is_file(), (
        f'{VENDORED_MARKED} is missing. chat.html loads it directly (#25); '
        f'without it markedReady stays false and answers render as plain text.'
    )


@pytest.mark.skipif(shutil.which('node') is None, reason='node not installed')
def test_chat_js_neutralises_raw_html_without_breaking_markdown():
    """XSS blocked, and C++ code samples still readable.

    Both halves matter. The first fix attempted here escaped the text before
    handing it to marked — safe, and it double-escaped every `<<` in the
    corpus, so a C++ course would have shipped `cout &lt;&lt; "hi"` to
    students. The check asserts both properties for that reason.
    """
    result = subprocess.run(
        ['node', str(CHECK)],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, (
        f'render_check.mjs failed:\n{result.stdout}\n{result.stderr}'
    )
