"""Tests for the corpus-directory concatenation behavior of load_group_context."""
from pathlib import Path

import pytest

from auth import load_group_context


def _setup_context(tmp_path: Path, monkeypatch) -> Path:
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    return tmp_path


def test_subdirectory_files_are_concatenated(tmp_path, monkeypatch):
    ctx = _setup_context(tmp_path, monkeypatch)
    (ctx / 'csc114_context.md').write_text('# Header\n')
    (ctx / 'csc114').mkdir()
    (ctx / 'csc114' / 'crosswalk.md').write_text('# Crosswalk body\n')

    result = load_group_context('csc114')

    assert '# Header' in result
    assert '=== CSC 114 CORPUS ===' in result
    assert '## crosswalk.md' in result
    assert '# Crosswalk body' in result
