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

    summary = apply_manifest(manifest, fetched, target)

    assert (target / 'crosswalk.md').read_text() == '# Crosswalk\n'
    assert (target / 'week-01' / 'lesson.md').read_text() == '# W1\n'
    assert (target / 'week-02' / 'lesson.md').read_text() == '# W2\n'
    assert not (target / 'unrelated.md').exists()
    assert summary == {
        'files': 3,
        'bytes': sum((target / p).stat().st_size for p in (
            'crosswalk.md', 'week-01/lesson.md', 'week-02/lesson.md'
        )),
    }


def test_apply_manifest_removes_stale_files(tmp_path):
    fetched = _make_fixture_upstream(tmp_path)
    target = tmp_path / 'target'
    target.mkdir()
    # A stale file from a previous sync that the new manifest does not include:
    stale = target / 'week-99' / 'old.md'
    stale.parent.mkdir(parents=True)
    stale.write_text('removed upstream')

    manifest = {
        'strip_prefix': 'planning/pilot_su26/',
        'paths': ['planning/pilot_su26/crosswalk.md'],
    }
    apply_manifest(manifest, fetched, target)

    assert not stale.exists()
    assert not (target / 'week-99').exists()  # empty dir pruned
    assert (target / 'crosswalk.md').exists()


def test_apply_manifest_raises_on_missing_upstream_path(tmp_path):
    fetched = _make_fixture_upstream(tmp_path)
    target = tmp_path / 'target'
    target.mkdir()
    manifest = {
        'strip_prefix': 'planning/pilot_su26/',
        'paths': ['planning/pilot_su26/week-99/'],  # not in fixture
    }
    with pytest.raises(FileNotFoundError, match='manifest path not in upstream'):
        apply_manifest(manifest, fetched, target)


def test_strip_prefix_without_trailing_slash_keeps_files_inside_target(tmp_path):
    """A manifest typo (missing trailing slash on strip_prefix) must not
    let stripped paths become absolute and escape the target directory."""
    fetched = _make_fixture_upstream(tmp_path)
    target = tmp_path / 'target'
    target.mkdir()
    manifest = {
        'strip_prefix': 'planning/pilot_su26',  # no trailing slash
        'paths': ['planning/pilot_su26/crosswalk.md'],
    }

    apply_manifest(manifest, fetched, target)

    assert (target / 'crosswalk.md').exists()
    # And nothing wrote to the filesystem root or anywhere outside target.
    assert not Path('/crosswalk.md').exists()


def test_strip_prefix_does_not_match_unrelated_component_boundary(tmp_path):
    """A strip_prefix that is a string-prefix but not a path-component prefix
    must not be stripped — otherwise 'planning/pilot' would consume part of
    'planning/pilot_su26'."""
    fetched = _make_fixture_upstream(tmp_path)
    target = tmp_path / 'target'
    target.mkdir()
    manifest = {
        'strip_prefix': 'planning/pilot',  # not a real component prefix
        'paths': ['planning/pilot_su26/crosswalk.md'],
    }

    apply_manifest(manifest, fetched, target)

    # File lands under the full path, not under a phantom '_su26/' directory.
    assert (target / 'planning' / 'pilot_su26' / 'crosswalk.md').exists()
    assert not (target / '_su26').exists()


def test_symlinks_inside_copied_directory_are_skipped(tmp_path):
    """Following symlinks from an external upstream into the vendored corpus
    is a supply-chain risk — the script must skip them."""
    fetched = _make_fixture_upstream(tmp_path)
    secret = tmp_path / 'secret.txt'
    secret.write_text('do not vendor this')
    (fetched / 'planning' / 'pilot_su26' / 'week-01' / 'poisoned.md').symlink_to(secret)

    target = tmp_path / 'target'
    target.mkdir()
    manifest = {
        'strip_prefix': 'planning/pilot_su26/',
        'paths': ['planning/pilot_su26/week-01/'],
    }

    apply_manifest(manifest, fetched, target)

    assert (target / 'week-01' / 'lesson.md').exists()
    assert not (target / 'week-01' / 'poisoned.md').exists()


def test_symlinked_manifest_path_is_rejected(tmp_path):
    """If a manifest entry itself points at a symlink, the script refuses."""
    fetched = _make_fixture_upstream(tmp_path)
    secret = tmp_path / 'secret.md'
    secret.write_text('elsewhere')
    (fetched / 'planning' / 'pilot_su26' / 'linked.md').symlink_to(secret)

    target = tmp_path / 'target'
    target.mkdir()
    manifest = {
        'strip_prefix': 'planning/pilot_su26/',
        'paths': ['planning/pilot_su26/linked.md'],
    }
    with pytest.raises(ValueError, match='refusing to follow'):
        apply_manifest(manifest, fetched, target)
