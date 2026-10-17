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


# ---------------------------------------------------------------------------
# Work package A1: local --source, map, transforms, deny, provenance.
# Synthetic fixtures only. Nothing below reads a real course repository.
# ---------------------------------------------------------------------------

import subprocess

from scripts.sync_course_corpus import (
    apply_map,
    deny_match,
    fence_text,
    html_to_markdown,
    local_source_sha,
)

_PAGE = """
<style>.x { color: red }</style>
<script>var leaked = "SCRIPT-BODY";</script>
<h2 style="color:#000">Page&nbsp;title &amp; more</h2>
<div style="padding:12px"><p style="margin:0">First <strong>bold</strong> and <em>soft</em> text with <code>x = 1</code>.</p></div>
<ul><li>apple</li><li>pear
  <ul><li>nested</li></ul></li></ul>
<ol><li>step one</li><li>step two</li></ol>
<details style="border:1px solid"><summary>Show the hint</summary><p>Hint body text.</p></details>
<table><tr><th>Name</th><th>Role</th></tr><tr><td>Ana</td><td>Analyst</td></tr></table>
<p><a href="https://example.com/a" style="color:blue">live link</a>
 <a href="https://example.com/LINK-PENDING-x">pending link</a>
 <a href="/relative/page">relative link</a></p>
<pre>line one
    indented   line</pre>
<h3>Next</h3>



<p>Last.</p>
"""


def test_html_to_markdown_converts_structure_and_strips_noise():
    md = html_to_markdown(_PAGE)

    assert md.startswith('## Page title & more\n')
    assert '### Next' in md
    assert 'First **bold** and *soft* text with `x = 1`.' in md
    # lists, including numbering and nesting
    assert '- apple' in md and '- pear' in md and '  - nested' in md
    assert '1. step one' in md and '2. step two' in md
    # a reveal keeps its summary (bold) and its body: student-visible
    assert '**Show the hint**' in md and 'Hint body text.' in md
    assert md.index('**Show the hint**') < md.index('Hint body text.')
    # table cells joined by ' | '
    assert 'Name | Role' in md and 'Ana | Analyst' in md
    # links: absolute http(s) kept, LINK-PENDING and relative reduced to text
    assert '[live link](https://example.com/a)' in md
    assert 'pending link' in md and 'LINK-PENDING' not in md
    assert 'relative link' in md and '/relative/page' not in md
    # <pre> keeps its whitespace inside a fence
    assert '```\nline one\n    indented   line\n```' in md
    # noise gone
    for needle in ('style', 'color', 'padding', 'SCRIPT-BODY', 'leaked', '<', '&nbsp;', '\xa0'):
        assert needle not in md, needle
    # at most one blank line anywhere
    assert '\n\n\n' not in md
    assert md.endswith('\n') and not md.endswith('\n\n')


def test_html_to_markdown_never_emits_a_style_attribute_for_any_tag():
    page = '<h2 style="a:b">T</h2><p style="a:b">x</p><span style="a:b">y</span><li style="a:b">z</li>'
    assert 'style' not in html_to_markdown(page)
    assert 'a:b' not in html_to_markdown(page)


def test_fence_wraps_with_language_and_survives_backticks_in_content():
    py = fence_text('print("hi")\n', '.py')
    assert py == '```python\nprint("hi")\n```\n'
    assert fence_text('plain', '.txt').startswith('```text\n')
    tricky = fence_text('a\n```\ninner\n```\n', '.py')
    # The fence must be longer than the longest run inside the content, or
    # the content closes its own fence and the rest escapes as prose.
    assert tricky.startswith('````python\n') and tricky.rstrip('\n').endswith('\n````')


@pytest.mark.parametrize('dest, rules, expected', [
    ('module-02/a.html', [{'from': 'module-02/', 'to': 'modules/m2/'}], 'modules/m2/a.html'),
    # component boundary: module-02x is a different directory
    ('module-02x/a.html', [{'from': 'module-02/', 'to': 'modules/m2/'}], 'module-02x/a.html'),
    ('module-02/x/a.html', [{'from': 'module-02', 'to': 'm2'}], 'm2/x/a.html'),
    # first match wins, so the specific rule must be listed first
    ('module-01/final-build/18-manual.html',
     [{'from': 'module-01/final-build/18-manual.html', 'to': 'reference/18-manual.html'},
      {'from': 'module-01/final-build/', 'to': 'modules/m1/'}],
     'reference/18-manual.html'),
    ('module-01/final-build/02-x.html',
     [{'from': 'module-01/final-build/18-manual.html', 'to': 'reference/18-manual.html'},
      {'from': 'module-01/final-build/', 'to': 'modules/m1/'}],
     'modules/m1/02-x.html'),
    ('other/a.md', [{'from': 'module-02/', 'to': 'm2/'}], 'other/a.md'),
    ('a.md', [], 'a.md'),
])
def test_apply_map(dest, rules, expected):
    assert apply_map(dest, rules) == expected


def test_map_and_transforms_through_apply_manifest(tmp_path):
    up = tmp_path / 'up'
    (up / 'module-02' / 'final-build').mkdir(parents=True)
    (up / 'module-02x').mkdir()
    (up / 'module-02' / 'final-build' / '01-page.html').write_text('<h2>One</h2><p>hi</p>')
    (up / 'module-02x' / 'keep.md').write_text('# keep\n')
    (up / 'starter').mkdir()
    (up / 'starter' / 'app.py').write_text('print(1)\n')
    (up / 'starter' / 'notes.txt').write_text('a note\n')
    target = tmp_path / 'target'
    manifest = {
        'strip_prefix': '',
        'paths': ['module-02/final-build/', 'module-02x/keep.md', 'starter/app.py',
                  'starter/notes.txt'],
        'map': [{'from': 'module-02/final-build/', 'to': 'modules/m2/'},
                {'from': 'starter/', 'to': 'modules/m5/starter/'}],
        'transforms': {'.html': 'html-to-markdown', '.py': 'fence', '.txt': 'fence'},
    }
    summary = apply_manifest(manifest, up, target)

    assert (target / 'modules/m2/01-page.md').read_text() == '## One\n\nhi\n'
    assert (target / 'modules/m5/starter/app.py.md').read_text() == '```python\nprint(1)\n```\n'
    assert (target / 'modules/m5/starter/notes.txt.md').read_text() == '```text\na note\n```\n'
    # untransformed and unmapped (module-02x is not module-02)
    assert (target / 'module-02x/keep.md').read_text() == '# keep\n'
    assert summary['transformed'] == 3 and summary['files'] == 4


def test_map_applies_after_strip_prefix(tmp_path):
    up = tmp_path / 'up'
    (up / 'root' / 'sub').mkdir(parents=True)
    (up / 'root' / 'sub' / 'a.md').write_text('a\n')
    target = tmp_path / 'target'
    apply_manifest({'strip_prefix': 'root/', 'paths': ['root/sub/'],
                    'map': [{'from': 'sub/', 'to': 'moved/'}]}, up, target)
    assert (target / 'moved' / 'a.md').exists()


def test_two_sources_mapped_to_one_destination_raise(tmp_path):
    up = tmp_path / 'up'
    (up / 'a').mkdir(parents=True)
    (up / 'b').mkdir()
    (up / 'a' / 'x.md').write_text('a\n')
    (up / 'b' / 'x.md').write_text('b\n')
    target = tmp_path / 'target'
    manifest = {'paths': ['a/x.md', 'b/x.md'],
                'map': [{'from': 'a/', 'to': 'm/'}, {'from': 'b/', 'to': 'm/'}]}
    with pytest.raises(ValueError, match='one destination'):
        apply_manifest(manifest, up, target)
    assert not list(target.rglob('*'))


def test_substitutions_run_on_transformed_output(tmp_path):
    up = tmp_path / 'up'
    up.mkdir()
    (up / 'p.html').write_text('<p>see PLANNING-DOC for more</p>')
    target = tmp_path / 'target'
    summary = apply_manifest(
        {'paths': ['p.html'], 'transforms': {'.html': 'html-to-markdown'},
         'substitutions': [{'pattern': 'PLANNING-DOC', 'replace': 'the module page'}]},
        up, target)
    assert (target / 'p.md').read_text() == 'see the module page for more\n'
    assert summary['rewrites'] == 1


# -- deny --------------------------------------------------------------------

_DENY = ['build-guides/', 'instructor-guides/', 'reference/', '*rubric*', '*-key.md',
         'M[0-9]-*.md', 'module-*/README.md', 'AGENTS.md']


def _deny_tree(tmp_path: Path) -> Path:
    up = tmp_path / 'up'
    for d in ('module-02/final-build', 'module-02/build-guides', 'module-07/reference',
              'module-09/a/b/build-guides/deep', 'module-02/student-facing'):
        (up / d).mkdir(parents=True)
    (up / 'module-02/final-build/01-page.html').write_text('<h2>ok</h2>')
    (up / 'module-02/student-facing/m2-template.md').write_text('# student\n')
    (up / 'module-02/build-guides/quiz-build.md').write_text('## Question 1 — x\n')
    (up / 'module-07/reference/schema.md').write_text('answers\n')
    (up / 'module-09/a/b/build-guides/deep/guide.md').write_text('deep\n')
    (up / 'module-02/M2-STAGE.md').write_text('# arch\n')
    (up / 'module-02/README.md').write_text('# readme\n')
    (up / 'module-02/final-build/grading-rubric.md').write_text('# rubric\n')
    (up / 'module-02/final-build/q-key.md').write_text('# key\n')
    (up / 'AGENTS.md').write_text('# agents\n')
    return up


def test_deny_list_is_nonempty_and_cases_exist():
    # An empty parametrize list is a silent pass. Pin the size.
    assert len(_DENY) >= 8


@pytest.mark.parametrize('listed', [
    'module-02/build-guides/quiz-build.md',        # directly listed file
    'module-02/build-guides/',                     # listed denied directory
    'module-02/',                                  # file inside a listed directory
    'module-09/',                                  # build-guides/ nested two levels down
    'module-09/a/b/build-guides/deep/guide.md',    # nested, listed directly
    'module-07/reference/schema.md',               # directory-name pattern, other dir
    'module-02/M2-STAGE.md',                       # filename glob
    'module-02/README.md',                         # whole-path glob
    'module-02/final-build/grading-rubric.md',     # *rubric*
    'module-02/final-build/q-key.md',              # *-key.md
    'AGENTS.md',                                   # bare filename
])
def test_deny_raises_and_writes_nothing(tmp_path, listed):
    up = _deny_tree(tmp_path)
    target = tmp_path / 'target'
    target.mkdir()
    # Put an allowed, earlier path in front: it must not be written either.
    manifest = {'paths': ['module-02/final-build/01-page.html', listed], 'deny': _DENY}
    with pytest.raises(ValueError, match='denied path in manifest'):
        apply_manifest(manifest, up, target)
    assert list(target.rglob('*')) == []


def test_deny_does_not_delete_existing_files_when_it_raises(tmp_path):
    up = _deny_tree(tmp_path)
    target = tmp_path / 'target'
    target.mkdir()
    (target / 'old.md').write_text('keep me\n')
    with pytest.raises(ValueError, match='denied path in manifest'):
        apply_manifest({'paths': ['module-02/build-guides/quiz-build.md'], 'deny': _DENY},
                       up, target)
    assert (target / 'old.md').read_text() == 'keep me\n'


def test_deny_allows_the_student_facing_file_it_must_not_confuse_with_m2_arch(tmp_path):
    """`M[0-9]-*.md` is case-sensitive: the student template `m2-template.md`
    is not the architecture record `M2-STAGE.md`."""
    up = _deny_tree(tmp_path)
    target = tmp_path / 'target'
    apply_manifest({'paths': ['module-02/student-facing/m2-template.md'], 'deny': _DENY},
                   up, target)
    assert (target / 'module-02/student-facing/m2-template.md').exists()


def test_deny_checks_upstream_path_not_the_mapped_destination(tmp_path):
    """`reference/` is both a denied upstream directory and a destination
    the manifest maps one page into. Only the upstream side is checked."""
    up = tmp_path / 'up'
    (up / 'module-01/final-build').mkdir(parents=True)
    (up / 'module-01/final-build/18-manual.html').write_text('<h2>Manual</h2>')
    target = tmp_path / 'target'
    manifest = {'paths': ['module-01/final-build/18-manual.html'], 'deny': _DENY,
                'map': [{'from': 'module-01/final-build/18-manual.html',
                         'to': 'reference/18-manual.html'}],
                'transforms': {'.html': 'html-to-markdown'}}
    apply_manifest(manifest, up, target)
    assert (target / 'reference/18-manual.md').read_text() == '## Manual\n'


def test_deny_refuses_dotdot_paths(tmp_path):
    up = _deny_tree(tmp_path)
    target = tmp_path / 'target'
    target.mkdir()
    with pytest.raises(ValueError, match=r'\.\.'):
        apply_manifest({'paths': ['module-02/final-build/../build-guides/quiz-build.md'],
                        'deny': _DENY}, up, target)
    assert list(target.rglob('*')) == []


@pytest.mark.parametrize('rel, is_dir, expected', [
    ('a/build-guides/x.md', False, 'build-guides/'),
    ('a/b/c/build-guides/d/e/x.md', False, 'build-guides/'),
    ('a/build-guides', True, 'build-guides/'),
    # a FILE named like a denied directory is not a directory component
    ('a/build-guides', False, None),
    ('a/build-guides-extra/x.md', False, None),
    ('a/b/x-key.md', False, '*-key.md'),
    ('a/M3-ARCH.md', False, 'M[0-9]-*.md'),
    ('a/m3-student.md', False, None),
    ('a/ok.md', False, None),
])
def test_deny_match(rel, is_dir, expected):
    patterns = ['build-guides/', '*-key.md', 'M[0-9]-*.md']
    assert deny_match(rel, patterns, is_dir) == expected


# -- local --source ----------------------------------------------------------

def _git(cwd: Path, *args: str) -> str:
    env = {'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@example.com',
           'GIT_COMMITTER_NAME': 't', 'GIT_COMMITTER_EMAIL': 't@example.com',
           'HOME': str(cwd), 'PATH': __import__('os').environ['PATH']}
    return subprocess.run(['git', '-C', str(cwd), *args], check=True, capture_output=True,
                          text=True, env=env).stdout.strip()


def _local_repo(tmp_path: Path) -> Path:
    repo = tmp_path / 'local_upstream'
    (repo / 'root').mkdir(parents=True)
    (repo / 'root' / 'only.md').write_text('# local\n')
    (repo / 'other.md').write_text('# other\n')
    _git(repo, 'init', '-q')
    _git(repo, 'add', '-A')
    _git(repo, 'commit', '-q', '-m', 'init')
    return repo


def _write_manifest(tmp_path: Path, target: Path, extra: str = '') -> Path:
    path = tmp_path / 'm.yaml'
    path.write_text(f"""
upstream: https://github.com/example/private
ref: main
target: {target}
strip_prefix: root/
paths:
  - root/only.md
{extra}""")
    return path


def test_source_uses_local_checkout_and_never_clones(tmp_path):
    repo = _local_repo(tmp_path)
    sha = _git(repo, 'rev-parse', 'HEAD')
    target = tmp_path / 'vendored'
    manifest = _write_manifest(tmp_path, target)
    with patch.object(sync_mod, 'fetch_upstream') as fetch, \
            patch.object(sync_mod.subprocess, 'run', wraps=sync_mod.subprocess.run) as run:
        rc = sync_mod.main(['--manifest', str(manifest), '--source', str(repo)])
    assert rc == 0
    fetch.assert_not_called()
    assert not any(c.args and 'clone' in c.args[0] for c in run.call_args_list)
    assert (target / 'only.md').read_text() == '# local\n'
    prov = (target / '_provenance.txt').read_text()
    assert f'source_sha: {sha}' in prov and len(sha) == 40
    assert 'upstream: https://github.com/example/private' in prov
    assert 'manifest: ' in prov


def test_source_rejects_uncommitted_change_under_a_manifest_path(tmp_path):
    repo = _local_repo(tmp_path)
    (repo / 'root' / 'only.md').write_text('# edited, not committed\n')
    target = tmp_path / 'vendored'
    manifest = _write_manifest(tmp_path, target)
    with patch.object(sync_mod, 'fetch_upstream') as fetch:
        with pytest.raises(ValueError, match='uncommitted changes'):
            sync_mod.main(['--manifest', str(manifest), '--source', str(repo)])
    fetch.assert_not_called()
    assert not target.exists() or not list(target.rglob('*'))


def test_source_rejects_untracked_file_under_a_manifest_path(tmp_path):
    repo = _local_repo(tmp_path)
    (repo / 'root' / 'new.md').write_text('untracked\n')
    with pytest.raises(ValueError, match='uncommitted changes'):
        local_source_sha(repo, ['root/'])


def test_source_ignores_dirt_outside_manifest_paths(tmp_path):
    repo = _local_repo(tmp_path)
    (repo / 'other.md').write_text('# dirty but not listed\n')
    assert len(local_source_sha(repo, ['root/only.md'])) == 40


def test_source_rejects_a_directory_that_is_not_a_git_repo(tmp_path):
    plain = tmp_path / 'plain'
    plain.mkdir()
    with pytest.raises(ValueError, match='not a git repository'):
        local_source_sha(plain, ['x'])


def test_source_rejects_a_subdirectory_of_a_repo(tmp_path):
    repo = _local_repo(tmp_path)
    with pytest.raises(ValueError, match='root of a git repository'):
        local_source_sha(repo / 'root', ['only.md'])


def test_provenance_survives_straggler_deletion(tmp_path):
    up = tmp_path / 'up'
    up.mkdir()
    (up / 'a.md').write_text('a\n')
    target = tmp_path / 'target'
    target.mkdir()
    (target / 'stale.md').write_text('stale\n')
    (target / 'sub').mkdir()
    (target / 'sub' / 'stale2.md').write_text('stale\n')
    summary = apply_manifest({'paths': ['a.md']}, up, target,
                             provenance={'source_sha': 'a' * 40, 'upstream': 'u'})
    assert (target / '_provenance.txt').read_text() == f"source_sha: {'a' * 40}\nupstream: u\n"
    assert not (target / 'stale.md').exists() and not (target / 'sub').exists()
    assert summary['files'] == 1          # provenance is not counted as corpus
    # a second sync keeps it too
    apply_manifest({'paths': ['a.md']}, up, target, provenance={'source_sha': 'b' * 40})
    assert ('b' * 40) in (target / '_provenance.txt').read_text()


def test_old_manifest_round_trips_with_no_provenance_and_no_new_files(tmp_path):
    """A manifest with none of map/transforms/deny and no --source behaves
    exactly as before: no _provenance.txt, same summary keys."""
    manifest = tmp_path / 'm.yaml'
    target = tmp_path / 'vendored'
    manifest.write_text(f"""
upstream: https://github.com/example/anything
ref: main
target: {target}
strip_prefix: root/
paths:
  - root/only.md
""")

    def fake_fetch(url, ref, dest):
        (dest / 'root').mkdir(parents=True)
        (dest / 'root' / 'only.md').write_text('# old path\n')

    with patch.object(sync_mod, 'fetch_upstream', side_effect=fake_fetch):
        assert sync_mod.main(['--manifest', str(manifest)]) == 0
    assert sorted(p.name for p in target.rglob('*')) == ['only.md']


def test_cloned_modern_manifest_also_records_provenance(tmp_path):
    """A manifest using deny/map/transforms gets provenance even through the
    clone path, so the corpus always says where it came from."""
    repo = _local_repo(tmp_path)
    target = tmp_path / 'vendored'
    manifest = _write_manifest(tmp_path, target, extra="deny:\n  - build-guides/\n")

    def fake_fetch(url, ref, dest):
        subprocess.run(['git', 'clone', '-q', str(repo), str(dest)], check=True)

    with patch.object(sync_mod, 'fetch_upstream', side_effect=fake_fetch):
        assert sync_mod.main(['--manifest', str(manifest)]) == 0
    assert _git(repo, 'rev-parse', 'HEAD') in (target / '_provenance.txt').read_text()
