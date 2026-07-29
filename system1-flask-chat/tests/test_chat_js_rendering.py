"""Runs the JavaScript render check, if node and marked are available.

The rendering path is the one piece of security-relevant logic in this repo
that Python cannot reach: `marked.parse()` output goes to `innerHTML`, and
marked has not sanitized since v5. A Python test can assert the source
*looks* right; only running it proves it.

Skips rather than fails when node or marked is missing, so a contributor
without a JS toolchain still gets a green suite. CI installs marked so the
check actually runs there — see .github/workflows/tests.yml.
"""
import shutil
import subprocess
from pathlib import Path

import pytest

CHECK = Path(__file__).resolve().parent / 'js' / 'render_check.mjs'
REPO_ROOT = Path(__file__).resolve().parents[2]


def _marked_available() -> bool:
    return (REPO_ROOT / 'node_modules' / 'marked').is_dir()


@pytest.mark.skipif(shutil.which('node') is None, reason='node not installed')
@pytest.mark.skipif(not _marked_available(), reason="marked not installed (npm install marked)")
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
