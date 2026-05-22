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


def test_non_markdown_files_are_skipped(tmp_path, monkeypatch):
    ctx = _setup_context(tmp_path, monkeypatch)
    (ctx / 'csc114_context.md').write_text('# Header\n')
    (ctx / 'csc114').mkdir()
    (ctx / 'csc114' / 'lesson.md').write_text('# Lesson\n')
    (ctx / 'csc114' / 'diagram.png').write_bytes(b'\x89PNG fake')
    (ctx / 'csc114' / 'notes.txt').write_text('plain text')

    result = load_group_context('csc114')

    assert '# Lesson' in result
    assert 'diagram.png' not in result
    assert 'plain text' not in result


def test_concatenation_order_is_sorted_by_relative_path(tmp_path, monkeypatch):
    ctx = _setup_context(tmp_path, monkeypatch)
    (ctx / 'csc114_context.md').write_text('# Header\n')
    base = ctx / 'csc114'
    (base / 'week-02').mkdir(parents=True)
    (base / 'week-01').mkdir(parents=True)
    (base / 'crosswalk.md').write_text('CROSSWALK\n')
    (base / 'week-01' / 'a.md').write_text('W1A\n')
    (base / 'week-01' / 'b.md').write_text('W1B\n')
    (base / 'week-02' / 'a.md').write_text('W2A\n')

    result = load_group_context('csc114')
    # crosswalk.md sorts before week-01/* which sorts before week-02/*
    order = [result.find(marker) for marker in
             ('CROSSWALK', 'W1A', 'W1B', 'W2A')]
    assert order == sorted(order)
    assert -1 not in order  # all markers present


def test_missing_main_context_raises_even_if_subdir_present(tmp_path, monkeypatch):
    ctx = _setup_context(tmp_path, monkeypatch)
    (ctx / 'csc114').mkdir()
    (ctx / 'csc114' / 'crosswalk.md').write_text('CROSSWALK\n')
    # NB: no csc114_context.md

    with pytest.raises(FileNotFoundError):
        load_group_context('csc114')
