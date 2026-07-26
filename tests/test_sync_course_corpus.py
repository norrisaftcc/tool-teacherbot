import re
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

import scripts.sync_course_corpus as sync_mod
from scripts.sync_course_corpus import apply_manifest, load_manifest


def test_both_course_manifests_load_and_share_schema():
    """Sanity check that both manifests parse and expose the required
    keys the sync script consumes — protects against a manifest typo
    silently breaking future runs."""
    root = Path(__file__).resolve().parent.parent / 'scripts'
    required = {'upstream', 'ref', 'target', 'paths', 'strip_prefix'}
    for name in ('csc114_manifest.yaml', 'csc134_manifest.yaml'):
        data = load_manifest(root / name)
        assert required <= set(data.keys()), f'{name} missing keys'
        assert isinstance(data['paths'], list) and data['paths']
        assert data['upstream'].startswith('https://github.com/')
        # csc134 upstream must point at the csc134 template repo, not
        # a copy-paste of csc114's — a mixup here silently vendors the
        # wrong course into the wrong skin.
        expected_repo = f'course-{name.split("_")[0]}-template'
        assert expected_repo in data['upstream']


def test_csc134_manifest_uses_haiku_target_dir(tmp_path):
    """The CSC 134 manifest must land its corpus in context/csc134/
    (not the CSC 114 dir — a copy-paste error would silently overwrite)."""
    root = Path(__file__).resolve().parent.parent / 'scripts'
    data = yaml.safe_load((root / 'csc134_manifest.yaml').read_text())
    assert data['target'].rstrip('/').endswith('/csc134')
    assert '/csc114' not in data['target']


def test_apply_manifest_works_for_csc134_shape(tmp_path):
    """Run the sync end-to-end against a fake upstream mirroring the
    CSC 134 manifest layout — proves the generalized script really is
    manifest-agnostic."""
    upstream = tmp_path / 'fake_csc134_upstream'
    (upstream / 'planning' / 'pilot_su26' / 'week-01').mkdir(parents=True)
    (upstream / 'planning' / 'pilot_su26' / 'week-02').mkdir(parents=True)
    (upstream / 'planning' / 'pilot_su26' / 'crosswalk.md').write_text('# 134\n')
    (upstream / 'planning' / 'pilot_su26' / 'week-01' / 'l.md').write_text('# 134 w1\n')
    (upstream / 'planning' / 'pilot_su26' / 'week-02' / 'l.md').write_text('# 134 w2\n')

    target = tmp_path / 'target_csc134'
    target.mkdir()
    manifest = {
        'strip_prefix': 'planning/pilot_su26/',
        'paths': [
            'planning/pilot_su26/crosswalk.md',
            'planning/pilot_su26/week-01/',
            'planning/pilot_su26/week-02/',
        ],
    }
    summary = apply_manifest(manifest, upstream, target)

    assert (target / 'crosswalk.md').read_text() == '# 134\n'
    assert (target / 'week-01' / 'l.md').exists()
    assert (target / 'week-02' / 'l.md').exists()
    assert summary['files'] == 3


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
        'excluded': 0,
        'rewrites': 0,
    }


def test_exclude_skips_instructor_files_inside_copied_dirs(tmp_path):
    """A course repo keeps answer keys next to the readings they answer.
    Vendoring one puts it in a student-facing bot's system prompt."""
    fetched = _make_fixture_upstream(tmp_path)
    week = fetched / 'planning' / 'pilot_su26' / 'week-01'
    (week / 'exit-ticket-key.md').write_text('# ANSWER KEY — do not hand to students')
    (week / '_assess-spec.STUB.md').write_text('# unauthored skeleton')

    target = tmp_path / 'target'
    target.mkdir()
    manifest = {
        'strip_prefix': 'planning/pilot_su26/',
        'paths': ['planning/pilot_su26/week-01/'],
        'exclude': ['**/*-key.md', '**/*.STUB.md'],
    }
    summary = apply_manifest(manifest, fetched, target)

    assert (target / 'week-01' / 'lesson.md').exists()
    assert not (target / 'week-01' / 'exit-ticket-key.md').exists()
    assert not (target / 'week-01' / '_assess-spec.STUB.md').exists()
    assert summary['excluded'] == 2


def test_exclude_skips_a_directly_listed_path(tmp_path):
    """Exclusion applies to explicit manifest entries too, not just files
    swept up by a directory copy."""
    fetched = _make_fixture_upstream(tmp_path)
    (fetched / 'planning' / 'pilot_su26' / 'solutions-key.md').write_text('# key')

    target = tmp_path / 'target'
    target.mkdir()
    manifest = {
        'strip_prefix': 'planning/pilot_su26/',
        'paths': [
            'planning/pilot_su26/crosswalk.md',
            'planning/pilot_su26/solutions-key.md',
        ],
        'exclude': ['**/*-key.md'],
    }
    summary = apply_manifest(manifest, fetched, target)

    assert (target / 'crosswalk.md').exists()
    assert not (target / 'solutions-key.md').exists()
    assert summary['files'] == 1


def test_absent_exclude_key_copies_everything(tmp_path):
    """Back-compat: a manifest without `exclude` behaves as before."""
    fetched = _make_fixture_upstream(tmp_path)
    target = tmp_path / 'target'
    target.mkdir()
    manifest = {
        'strip_prefix': 'planning/pilot_su26/',
        'paths': ['planning/pilot_su26/week-01/'],
    }
    summary = apply_manifest(manifest, fetched, target)

    assert (target / 'week-01' / 'lesson.md').exists()
    assert summary['excluded'] == 0


def test_substitutions_rewrite_vendored_markdown(tmp_path):
    """We vendor a subset of a repo whose documents assume the whole repo,
    so cross-references can point at files that exist upstream and not
    here. Observed live: the bot sent a student to a _tracking/ path."""
    fetched = _make_fixture_upstream(tmp_path)
    week = fetched / 'planning' / 'pilot_su26' / 'week-01'
    (week / 'notes.md').write_text(
        'Per `_tracking/skeleton-plan.md` the rule holds.\n'
        'See the [course manifest](../_tracking/manifest.yaml) for status.\n'
    )

    target = tmp_path / 'target'
    target.mkdir()
    manifest = {
        'strip_prefix': 'planning/pilot_su26/',
        'paths': ['planning/pilot_su26/week-01/'],
        'substitutions': [
            {'pattern': r'\[([^\]]+)\]\(/?(?:\.\./)*_tracking/[^)]*\)',
             'replace': r'\1'},
            {'pattern': '`/?_tracking/[^`]*`', 'replace': 'a planning doc'},
        ],
    }
    summary = apply_manifest(manifest, fetched, target)

    out = (target / 'week-01' / 'notes.md').read_text()
    assert 'Per a planning doc the rule holds.' in out
    assert 'See the course manifest for status.' in out
    assert '_tracking' not in out
    assert summary['rewrites'] == 2


def test_link_substitution_runs_before_target_substitution(tmp_path):
    """Ordering regression: rewriting a link *target* first leaves a
    still-broken `[label](prose)`. The first pass of this feature shipped
    exactly that bug."""
    fetched = _make_fixture_upstream(tmp_path)
    (fetched / 'planning' / 'pilot_su26' / 'week-01' / 'notes.md').write_text(
        'See the [manifest](../_tracking/manifest.yaml).\n')

    target = tmp_path / 'target'
    target.mkdir()
    manifest = {
        'strip_prefix': 'planning/pilot_su26/',
        'paths': ['planning/pilot_su26/week-01/'],
        'substitutions': [
            {'pattern': r'\[([^\]]+)\]\(/?(?:\.\./)*_tracking/[^)]*\)',
             'replace': r'\1'},
            {'pattern': '/?_tracking/[A-Za-z0-9_.-]+', 'replace': 'a planning doc'},
        ],
    }
    apply_manifest(manifest, fetched, target)

    out = (target / 'week-01' / 'notes.md').read_text()
    assert out.strip() == 'See the manifest.'
    assert '](' not in out, 'a markdown link whose target became prose'


def test_absent_substitutions_key_leaves_content_untouched(tmp_path):
    fetched = _make_fixture_upstream(tmp_path)
    target = tmp_path / 'target'
    target.mkdir()
    manifest = {
        'strip_prefix': 'planning/pilot_su26/',
        'paths': ['planning/pilot_su26/week-01/'],
    }
    summary = apply_manifest(manifest, fetched, target)

    assert (target / 'week-01' / 'lesson.md').read_text() == '# W1\n'
    assert summary['rewrites'] == 0


def test_vendored_csc134_corpus_has_no_upstream_only_links():
    """Guard on what actually landed: a re-sync with a broken substitution
    would otherwise quietly restore the dead pointers."""
    corpus = (Path(__file__).resolve().parent.parent
              / 'system1-flask-chat' / 'context' / 'csc134')
    if not corpus.is_dir():
        pytest.skip('csc134 corpus not vendored in this checkout')
    offenders = [
        p for p in corpus.rglob('*.md')
        if re.search(r'_(tracking|contracts|storming)/', p.read_text(encoding='utf-8'))
    ]
    assert not offenders, f'upstream-only paths still referenced: {offenders}'


def test_load_manifest_reads_utf8_regardless_of_platform_encoding(tmp_path):
    """read_text() defaults to the platform encoding, so on Windows an em
    dash in a substitution round-tripped through cp1252 and landed in the
    corpus as "â€”". Shipped once; guarded now."""
    manifest_path = tmp_path / 'm.yaml'
    manifest_path.write_text(
        "upstream: https://github.com/example/x\n"
        "ref: main\n"
        "target: out\n"
        "strip_prefix: ''\n"
        "paths: ['a.md']\n"
        "substitutions:\n"
        "  - pattern: 'x'\n"
        "    replace: 'the Mail Run — stage, commit, push'\n",
        encoding='utf-8',
    )
    data = load_manifest(manifest_path)
    assert data['substitutions'][0]['replace'] == 'the Mail Run — stage, commit, push'


def test_vendored_csc134_m0_has_no_pull_request_walkthrough():
    """CSC 134 first-years submit with the Mail Run and are not shown a PR.
    Upstream marks the walkthrough DO NOT PORT / superseded; the course
    lead confirms it. A re-sync that lost the exclusion would put it back
    in front of week-1 students."""
    m0 = (Path(__file__).resolve().parent.parent / 'system1-flask-chat'
          / 'context' / 'csc134')
    if not m0.is_dir():
        pytest.skip('csc134 corpus not vendored in this checkout')
    assert not (m0 / 'assignments' / 'm0' / '02_first_pull_request.md').exists()
    window = list((m0 / 'assignments' / 'm0').glob('*.md'))
    window += list((m0 / 'modules' / 'm0').glob('*.md'))
    offenders = [p for p in window
                 if 'pull request' in p.read_text(encoding='utf-8').lower()]
    assert not offenders, f'PR material still in the m0 window: {offenders}'


def test_csc134_manifest_excludes_instructor_facing_files():
    """Regression guard on the shipped manifest: the first sync vendored
    modules/m4/practice-exit-ticket-key.md — an answer key headed
    'Do not hand to students' — into a student-facing corpus."""
    root = Path(__file__).resolve().parent.parent / 'scripts'
    data = load_manifest(root / 'csc134_manifest.yaml')
    assert '**/*-key.md' in data['exclude']


def test_vendored_csc134_corpus_has_no_instructor_facing_files():
    """Belt and braces: assert on what actually landed on disk, not just
    what the manifest says. A future manual edit could reintroduce one."""
    corpus = (Path(__file__).resolve().parent.parent
              / 'system1-flask-chat' / 'context' / 'csc134')
    if not corpus.is_dir():
        pytest.skip('csc134 corpus not vendored in this checkout')
    offenders = [
        p for p in corpus.rglob('*.md')
        if 'audience: instructor' in p.read_text(encoding='utf-8').lower()
    ]
    assert not offenders, f'instructor-facing files vendored: {offenders}'


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


def test_main_cli_routes_manifest_flag_to_apply_manifest(tmp_path):
    """End-to-end CLI test: main(['--manifest', X]) must load X,
    invoke fetch_upstream with X's upstream/ref, and apply the manifest
    into the target dir. Covers argparse + manifest resolution + the
    plumbing that T2 added (untested by the apply_manifest-only cases)."""
    manifest_path = tmp_path / 'test_manifest.yaml'
    target = tmp_path / 'vendored'
    manifest_path.write_text(f"""
upstream: https://github.com/example/anything
ref: main
target: {target}
strip_prefix: root/
paths:
  - root/only.md
""")

    def fake_fetch(url, ref, dest):
        assert url == 'https://github.com/example/anything'
        assert ref == 'main'
        (dest / 'root').mkdir(parents=True)
        (dest / 'root' / 'only.md').write_text('# from CLI\n')

    with patch.object(sync_mod, 'fetch_upstream', side_effect=fake_fetch):
        rc = sync_mod.main(['--manifest', str(manifest_path)])

    assert rc == 0
    assert (target / 'only.md').read_text() == '# from CLI\n'
