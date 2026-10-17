"""The CTS-285 corpus is student-visible material only. Prove it on disk.

The cts285 skin answers students. Whatever is vendored under
`system1-flask-chat/context/cts285/` can reach the system prompt, where no
persona wording reliably holds an answer key back. So this file asserts on
the FILES THEMSELVES, not on the manifest that produced them: the manifest
can be correct while a hand-copied build guide sits in the directory.

Two things are deliberately not skippable here. The corpus directory must
exist (an absent corpus is a failure, not a skip: a guard that skips when
the thing is missing passes in exactly the situation it exists for), and
every loop asserts it scanned at least one file (an empty scan is a silent
pass).

The upstream repository is private and is not available in CI, so nothing
here reads it. The tests read the manifest and the vendored output only.
"""
import re
from pathlib import Path, PurePosixPath

import pytest

import scripts.sync_course_corpus as sync_mod
from scripts.sync_course_corpus import apply_map, deny_match, load_manifest

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / 'scripts' / 'cts285_manifest.yaml'
CORPUS = REPO / 'system1-flask-chat' / 'context' / 'cts285'

# Every pattern the deny list must carry. A weaker list is a regression even
# when the current `paths` happens to avoid the hole.
REQUIRED_DENY = [
    'build-guides/', 'instructor-guides/', 'planning/', 'reference/',
    'review-target/', 'exemplars/', 'failure-variants/', 'binder/',
    'assignments/', 'assessments/', 'instructor-workflows/', 'style/',
    'docs/', 'course-level/', 'resources/',
    '*rubric*', '*answer-key*', '*-key.md', 'M[0-9]-*.md',
    '00-START-HERE.md', 'AGENTS.md', 'CLAUDE.md',
]

# (upstream path that must be refused, why). One representative per pattern,
# nested two levels deep where the pattern is a directory, because a
# directory guard that only sees the top level is the defect.
MUST_BE_DENIED = [
    'module-02/build-guides/requirement-triage-lab-new-quiz-build.md',
    'module-02/deep/nest/build-guides/x.md',
    'module-02/instructor-guides/period-1.md',
    'planning/DECISIONS.md',
    'module-07/reference/data_store.py',
    'module-06/review-target/app.py',
    'module-06/exemplars/sample.md',
    'module-07/student-facing/failure-variants/data_store-load-reseeds.py',
    'binder/cts285-answer-key.html',
    'module-04/assignments/m4-lab-evidence-record-rubric.md',
    'module-04/assessments/quiz.md',
    'instructor-workflows/norris-weekly-delivery-workflow.md',
    'style/CANVAS-HOUSE-STYLE.md',
    'docs/COLLABORATIVE-BUILD-GLOSSARY.md',
    'course-level/pattern-guide.md',
    'module-01/resources/dataman-manual.md',
    'module-03/final-build/some-rubric.html',
    'module-06/build-guides/m6-review-target-key.md',
    'module-02/student-facing/thing-answer-key.md',
    'module-02/M2-STAGE-REALIGNMENT.md',
    '00-START-HERE.md',
    'module-02/00-START-HERE.md',
    'module-02/README.md',
    'module-0-getting-started/README.md',
    'AGENTS.md',
    'CLAUDE.md',
    'module-02/final-build/11-m2-3a-interview-ms-alvarez.html',
    'module-02/final-build/12-m2-3b-premature-solution.html',
    'module-02/final-build/13-m2-3c-observe-a-practice-session.html',
    'module-02/final-build/14-m2-3d-review-the-manual.html',
    'module-02/final-build/15-m2-3e-what-did-you-surface.html',
]

# Names that must not appear anywhere under the vendored tree.
FORBIDDEN_NAME = re.compile(
    r'build-guide|instructor|rubric|answer-key|-key\b|review-target|exemplar|'
    r'failure-variant|m2-3[a-e]', re.I)

# Content that appears only in build guides, rubrics, keys and instructor
# material (verified absent from every student-visible file, 2026-10-17).
FORBIDDEN_CONTENT = [
    re.compile(r'^## Question \d+ —', re.M),
    re.compile(r'## Points check'),
    re.compile(r'^## Criterion \d+ —', re.M),
    re.compile(r'## Canvas setup notes'),
    re.compile(r'## Recommended settings'),
    re.compile(r'Correct answer:'),
    re.compile(r'\*\*CORRECT\*\*'),
    re.compile(r'audience: instructor'),
    re.compile(r'Norris'),
    re.compile(r'DataMan Corp'),
    re.compile(r'style='),
]


@pytest.fixture(scope='module')
def manifest():
    return load_manifest(MANIFEST)


def _mapped(manifest, rel):
    """Destination of one manifest path, exactly as the sync computes it."""
    dest = apply_map(rel, list(manifest.get('map') or []))
    mode = {k.lower(): v for k, v in manifest['transforms'].items()}.get(PurePosixPath(rel).suffix.lower())
    p = PurePosixPath(dest)
    if mode == 'html-to-markdown':
        p = p.with_suffix('.md')
    elif mode == 'fence':
        p = p.with_name(p.name + '.md')
    return p.as_posix()


def _vendored():
    files = [p for p in CORPUS.rglob('*') if p.is_file()]
    assert files, 'no files under context/cts285: the scan below would be empty'
    return files


# ---------------------------------------------------------------------------
# The manifest
# ---------------------------------------------------------------------------

def test_manifest_shape(manifest):
    assert {'upstream', 'ref', 'target', 'paths', 'strip_prefix', 'deny', 'map',
            'transforms'} <= set(manifest)
    assert manifest['target'].rstrip('/').endswith('/cts285')
    assert manifest['upstream'].startswith('https://github.com/')
    assert manifest['paths'], 'empty allow-list'
    assert len(set(manifest['paths'])) == len(manifest['paths']), 'duplicate path'


def test_paths_are_files_not_directories(manifest):
    """An allow-list of directories is a deny-list in disguise: whatever is
    added to a directory upstream is vendored without anyone deciding."""
    assert manifest['paths']
    for p in manifest['paths']:
        assert PurePosixPath(p).suffix, f'{p} looks like a directory, list files'
        assert not p.endswith('/')


def test_deny_carries_every_required_pattern(manifest):
    assert REQUIRED_DENY
    missing = [p for p in REQUIRED_DENY if p not in manifest['deny']]
    assert not missing, f'deny list lost: {missing}'
    # The README pattern is spelled so it does not also deny the M5 starter README.
    assert any(p.startswith('module-') and p.endswith('README.md') for p in manifest['deny'])


def test_every_path_passes_the_deny_guard(manifest):
    checked = 0
    for p in manifest['paths']:
        hit = deny_match(sync_mod._posix(p), manifest['deny'])
        assert hit is None, f'allow-listed path {p} matches deny pattern {hit!r}'
        checked += 1
    assert checked == len(manifest['paths']) > 0


@pytest.mark.parametrize('rel', MUST_BE_DENIED)
def test_deny_refuses_representative_path(manifest, rel):
    assert deny_match(rel, manifest['deny']) is not None, f'{rel} would be vendored'


def test_must_be_denied_is_not_empty():
    assert len(MUST_BE_DENIED) > 20


def test_deny_does_not_swallow_the_m5_starter_readme(manifest):
    """`module-*/README.md` under fnmatch crosses `/` and would. The starter
    README is student-visible and is on the allow-list."""
    readme = 'module-05/starter/minimal-flask-app/README.md'
    assert readme in manifest['paths']
    assert deny_match(readme, manifest['deny']) is None


def test_retired_m2_case_pages_are_not_listed(manifest):
    listed = [p for p in manifest['paths'] if re.search(r'm2-3[a-e]-', p)]
    assert listed == []
    assert manifest['paths']


# ---------------------------------------------------------------------------
# The vendored files on disk
# ---------------------------------------------------------------------------

def test_corpus_directory_exists():
    # assert, never skip: see the module docstring
    assert CORPUS.is_dir(), f'{CORPUS} is missing'


@pytest.mark.parametrize('n', range(9))
def test_each_module_window_holds_markdown(n):
    window = CORPUS / 'modules' / f'm{n}'
    assert window.is_dir(), f'{window} missing'
    assert list(window.rglob('*.md')), f'{window} holds no .md'


def test_disk_matches_manifest_exactly(manifest):
    """Same set both ways. Extra file: something was copied in by hand (or a
    deny hole let it through). Missing file: the corpus is stale."""
    expected = {_mapped(manifest, p) for p in manifest['paths']}
    on_disk = {p.relative_to(CORPUS).as_posix() for p in _vendored()} - {'_provenance.txt'}
    assert expected
    assert on_disk - expected == set(), f'on disk, not in manifest: {sorted(on_disk - expected)}'
    assert expected - on_disk == set(), f'in manifest, not on disk: {sorted(expected - on_disk)}'


def test_only_markdown_and_provenance_on_disk():
    """The corpus loader reads *.md. Anything else is dead weight or a file
    nobody meant to vendor."""
    odd = [p.relative_to(CORPUS).as_posix() for p in _vendored()
           if p.suffix != '.md' and p.name != '_provenance.txt']
    assert odd == []


def test_manual_is_present_and_says_two_tries():
    manual = CORPUS / 'reference' / '18-the-dataman-manual.md'
    assert manual.is_file()
    text = manual.read_text(encoding='utf-8')
    assert 'two tries' in text
    assert not re.search(r'three (tries|attempts)', text, re.I)


def test_no_vendored_file_is_named_like_instructor_material():
    names = [p.relative_to(CORPUS).as_posix() for p in _vendored()]
    assert names
    bad = [n for n in names if FORBIDDEN_NAME.search(n)]
    assert bad == []


def test_no_vendored_file_has_instructor_content():
    scanned = 0
    for p in _vendored():
        if p.suffix != '.md':
            continue
        text = p.read_text(encoding='utf-8')
        scanned += 1
        for rx in FORBIDDEN_CONTENT:
            m = rx.search(text)
            assert m is None, f'{p.relative_to(CORPUS)} matches {rx.pattern!r}: {m.group(0)!r}'
    assert scanned > 100, f'only {scanned} files scanned'


def test_no_unrendered_html_or_canvas_build_note_survived():
    scanned = 0
    for p in _vendored():
        if p.suffix != '.md':
            continue
        text = p.read_text(encoding='utf-8')
        scanned += 1
        assert 'LINK-PENDING' not in text, p
        assert 'CANVAS BUILD NOTE' not in text, p
        assert '<!--' not in text, p
    assert scanned > 100


def test_provenance_records_a_full_sha(manifest):
    prov = CORPUS / '_provenance.txt'
    assert prov.is_file()
    fields = dict(line.split(': ', 1) for line in prov.read_text(encoding='utf-8').splitlines())
    assert re.fullmatch(r'[0-9a-f]{40}', fields['source_sha'])
    assert fields['upstream'] == manifest['upstream']
    assert fields['manifest'] == 'scripts/cts285_manifest.yaml'
