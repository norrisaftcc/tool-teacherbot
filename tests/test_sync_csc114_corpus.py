from pathlib import Path
import pytest

from scripts.sync_csc114_corpus import apply_manifest


def _make_fixture_upstream(tmp_path: Path) -> Path:
    """Build a fake upstream tree we can copy from."""
    root = tmp_path / 'fake_upstream'
    (root / 'planning' / 'pilot_su26' / 'week-01').mkdir(parents=True)
    (root / 'planning' / 'pilot_su26' / 'week-02').mkdir(parents=True)
    (root / 'planning' / 'pilot_su26' / 'crosswalk.md').write_text('# Crosswalk\n')
    (root / 'planning' / 'pilot_su26' / 'week-01' / 'lesson.md').write_text('# W1\n')
    (root / 'planning' / 'pilot_su26' / 'week-02' / 'lesson.md').write_text('# W2\n')
    (root / 'unrelated.md').write_text('do not copy me')
    return root


def test_apply_manifest_copies_listed_paths(tmp_path):
    fetched = _make_fixture_upstream(tmp_path)
    target = tmp_path / 'target'
    target.mkdir()
    manifest = {
        'strip_prefix': 'planning/pilot_su26/',
        'paths': [
            'planning/pilot_su26/crosswalk.md',
            'planning/pilot_su26/week-01/',
            'planning/pilot_su26/week-02/',
        ],
    }

    apply_manifest(manifest, fetched, target)

    assert (target / 'crosswalk.md').read_text() == '# Crosswalk\n'
    assert (target / 'week-01' / 'lesson.md').read_text() == '# W1\n'
    assert (target / 'week-02' / 'lesson.md').read_text() == '# W2\n'
    assert not (target / 'unrelated.md').exists()
