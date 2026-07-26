# tests/test_auth.py
import pytest
from auth import (
    SKINS,
    active_module,
    authenticate_skin,
    load_skin_context,
    load_skin_persona,
    module_window,
)


def _paired_corpus(tmp_path, module='m0'):
    """Lay out a csc134-shaped corpus: upstream splits a week across
    modules/mN (what it's about) and assignments/mN (what you do)."""
    (tmp_path / 'csc134_context.md').write_text('# header')
    corpus = tmp_path / 'csc134'
    (corpus / 'outline').mkdir(parents=True)
    (corpus / 'modules' / module).mkdir(parents=True)
    (corpus / 'assignments' / module).mkdir(parents=True)
    (corpus / 'outline' / 'topics.md').write_text('# outline body')
    (corpus / 'modules' / module / '_overview.md').write_text('# module body')
    (corpus / 'assignments' / module / '01_setup.md').write_text('# assignment body')
    return corpus


def _window(tmp_path, slug='csc114', module='week-02-keras-hello-world'):
    """Build a corpus laid out like the real one: an index file, the active
    module, and a stale module that must stay out of the prompt."""
    (tmp_path / f'{slug}_context.md').write_text('# header')
    corpus = tmp_path / slug
    (corpus / module).mkdir(parents=True)
    (corpus / 'week-01-cloud-agents').mkdir(parents=True)
    (corpus / 'crosswalk.md').write_text('# crosswalk body')
    (corpus / module / 'learn.md').write_text('# active body')
    (corpus / 'week-01-cloud-agents' / 'learn.md').write_text('# stale body')
    return corpus


# ---- new-contract (SKINS) --------------------------------------------------

def test_csc114_skin_present():
    assert 'csc114' in SKINS
    assert SKINS['csc114']['password'] == '2026su'
    assert SKINS['csc114']['clearance'] == 'ORANGE'
    assert SKINS['csc114']['model'] == 'claude-sonnet-4-6'


def test_csc134_skin_present_on_haiku():
    assert 'csc134' in SKINS
    assert SKINS['csc134']['model'] == 'claude-haiku-4-5-20251001'
    assert SKINS['csc134']['password']  # must be set (placeholder OK)


def test_authenticate_skin_valid():
    s = authenticate_skin('csc114', '2026su')
    assert s is not None
    assert s['model'] == 'claude-sonnet-4-6'


def test_authenticate_skin_bad_password():
    assert authenticate_skin('csc114', 'wrong') is None


def test_authenticate_skin_unknown_slug():
    assert authenticate_skin('nope', '2026su') is None


def test_load_skin_context_returns_header(tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# CSC 114 header')
    out = load_skin_context('csc114')
    assert '# CSC 114 header' in out


def test_load_skin_context_appends_index_and_active_module(tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    _window(tmp_path)

    out = load_skin_context('csc114')

    assert '# header' in out
    assert '# crosswalk body' in out          # corpus_index
    assert '# active body' in out             # active_module
    assert '--- corpus: week-02-keras-hello-world/learn.md ---' in out


def test_load_skin_context_excludes_inactive_modules(tmp_path, monkeypatch):
    """The whole point of ADR-0002: a module that is not the active one
    stays vendored on disk and out of the system prompt."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    _window(tmp_path)

    out = load_skin_context('csc114')

    assert '# stale body' not in out
    assert 'week-01-cloud-agents' not in out


def test_active_module_env_override_wins(tmp_path, monkeypatch):
    """A course lead advances the week from the Render dashboard."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    _window(tmp_path)
    monkeypatch.setenv('CSC114_ACTIVE_MODULE', 'week-01-cloud-agents')

    assert active_module('csc114') == 'week-01-cloud-agents'
    out = load_skin_context('csc114')
    assert '# stale body' in out       # now the active one
    assert '# active body' not in out  # now the inactive one


def test_active_module_env_override_ignores_bogus_value(tmp_path, monkeypatch):
    """A typo in a dashboard field must not silently empty the corpus."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    _window(tmp_path)
    monkeypatch.setenv('CSC114_ACTIVE_MODULE', 'week-99-does-not-exist')

    assert active_module('csc114') == SKINS['csc114']['active_module']
    assert '# active body' in load_skin_context('csc114')


def test_active_module_env_override_cannot_escape_corpus(tmp_path, monkeypatch):
    """`../` in the override must not reach outside the corpus dir."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    _window(tmp_path)
    (tmp_path / 'elsewhere').mkdir()
    (tmp_path / 'elsewhere' / 'secret.md').write_text('do-not-vendor-me')
    monkeypatch.setenv('CSC114_ACTIVE_MODULE', '../elsewhere')

    assert active_module('csc114') == SKINS['csc114']['active_module']
    assert 'do-not-vendor-me' not in load_skin_context('csc114')


def test_load_skin_context_survives_missing_module(tmp_path, monkeypatch):
    """A corpus that hasn't been synced yet degrades to header-only rather
    than 500ing a student's login."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# header')
    (tmp_path / 'csc114').mkdir()

    out = load_skin_context('csc114')
    assert out.strip() == '# header'


# ---- paired module window (ADR-0002 amendment) -----------------------------

def test_module_window_expands_every_template():
    assert module_window('csc134') == [
        f'modules/{SKINS["csc134"]["active_module"]}',
        f'assignments/{SKINS["csc134"]["active_module"]}',
    ]
    # csc114's modules are top-level dirs — one template, unchanged.
    assert module_window('csc114') == [SKINS['csc114']['active_module']]


def test_csc134_window_carries_module_and_assignments(tmp_path, monkeypatch):
    """The gap the first sync exposed: modules/m0 says what the week is
    about, assignments/m0 is the workspace-setup walkthrough a week-1
    student actually asks about. The window needs both."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    _paired_corpus(tmp_path)

    out = load_skin_context('csc134')

    assert '# outline body' in out       # index
    assert '# module body' in out        # modules/m0
    assert '# assignment body' in out    # assignments/m0
    assert '--- corpus: assignments/m0/01_setup.md ---' in out


def test_module_without_assignments_still_loads(tmp_path, monkeypatch):
    """m3-m8 have readings but no assignments authored yet. A half-present
    module is a normal state, not a failure."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    corpus = _paired_corpus(tmp_path, module='m3')
    import shutil
    shutil.rmtree(corpus / 'assignments' / 'm3')
    monkeypatch.setenv('CSC134_ACTIVE_MODULE', 'm3')

    out = load_skin_context('csc134')

    assert active_module('csc134') == 'm3'
    assert '# module body' in out


def test_module_with_only_assignments_still_loads(tmp_path, monkeypatch):
    """The mirror case: an assignment authored before its module page."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    corpus = _paired_corpus(tmp_path, module='m7')
    import shutil
    shutil.rmtree(corpus / 'modules' / 'm7')
    monkeypatch.setenv('CSC134_ACTIVE_MODULE', 'm7')

    assert active_module('csc134') == 'm7'
    assert '# assignment body' in load_skin_context('csc134')


def test_env_override_takes_a_bare_module_id(tmp_path, monkeypatch):
    """The override a course lead types into Render is `m3`, not a path."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    _paired_corpus(tmp_path, module='m3')
    monkeypatch.setenv('CSC134_ACTIVE_MODULE', 'm3')

    assert active_module('csc134') == 'm3'
    assert module_window('csc134') == ['modules/m3', 'assignments/m3']


def test_every_csc134_module_window_clears_the_haiku_cache_floor():
    """Haiku 4.5 will not cache a prefix under 4096 tokens — silently, with
    no error. ADR-0002's cost model assumes every module window caches, so
    a corpus edit that thins a window below the floor is a real regression
    that nothing else would catch.

    Estimated at bytes/4; spot-checked against a real tokenizer at
    0.97-1.04x, so the estimate is sound to a few percent. The thinnest
    windows (m3, m5-m7) clear the floor by only 163-728 tokens, which is
    exactly why this guard exists.
    """
    import os
    import auth
    import claude_handler

    corpus = auth.CONTEXT_DIR / 'csc134'
    if not corpus.is_dir():
        pytest.skip('csc134 corpus not vendored in this checkout')

    persona = load_skin_persona('csc134')
    previous = os.environ.get('CSC134_ACTIVE_MODULE')
    thin = {}
    try:
        for module_dir in sorted((corpus / 'modules').iterdir()):
            if not module_dir.is_dir():
                continue
            os.environ['CSC134_ACTIVE_MODULE'] = module_dir.name
            prompt = claude_handler.build_system_prompt(
                load_skin_context('csc134'), persona)
            estimate = len(prompt) // 4
            if estimate < 4096:
                thin[module_dir.name] = estimate
    finally:
        os.environ.pop('CSC134_ACTIVE_MODULE', None)
        if previous is not None:
            os.environ['CSC134_ACTIVE_MODULE'] = previous

    assert not thin, (
        f'module windows below the 4096-token cache floor: {thin} — these '
        f'would silently stop caching for the whole cohort'
    )


def test_csc134_active_module_is_an_id_not_a_path():
    """Regression guard: `modules/m0` here would expand to
    `modules/modules/m0` and silently window nothing."""
    assert '/' not in (SKINS['csc134']['active_module'] or '')


# ---- persona ---------------------------------------------------------------

def test_load_skin_persona_returns_file(tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc134_persona.md').write_text('# be an intro C++ TA')
    assert '# be an intro C++ TA' in load_skin_persona('csc134')


def test_load_skin_persona_missing_raises(tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    with pytest.raises(FileNotFoundError):
        load_skin_persona('csc134')


def test_load_skin_persona_unknown_slug_raises():
    with pytest.raises(KeyError):
        load_skin_persona('bogus')


def test_every_skin_has_shipped_persona_and_header_files():
    """The registry points at real files — a rename that misses one would
    otherwise only surface when a student tries to log in."""
    import auth
    for slug, skin in SKINS.items():
        assert (auth.CONTEXT_DIR / skin['persona_file']).is_file(), slug
        assert (auth.CONTEXT_DIR / skin['header_file']).is_file(), slug


def test_csc134_persona_is_not_algocratic():
    """CSC 134 is intro C++, not the AlgoCratic capstone — the whole point
    of ADR-0002's persona split."""
    persona = load_skin_persona('csc134')
    assert 'AlgoCratic' not in persona
    assert 'The Algorithm' not in persona


def test_csc134_teaching_notes_are_precise_about_warning_vs_error():
    """Split out of the instructor answer keys, which stay out of the corpus
    because they carry the answers. The pedagogy in them does not.

    The precision here is load-bearing: a student at a terminal can falsify
    the bot in one command, and the first run of the eval bank caught it
    claiming g++ warns about a missing semicolon. It errors."""
    from auth import load_skin_notes
    notes = load_skin_notes('csc134')
    assert 'Warning is not error' in notes
    assert '-Wempty-body' in notes, 'the stray-semicolon case that really warns'
    assert 'do not guess' in notes.lower()
    for name in ('Syntax', 'Static semantic', 'Runtime', 'Logic'):
        assert name in notes, name


def test_csc114_declares_no_teaching_notes():
    """Notes are optional. A skin without them composes a prompt with no
    empty HOW THIS COURSE TEACHES heading."""
    import claude_handler
    from auth import load_skin_notes
    assert load_skin_notes('csc114') == ''
    prompt = claude_handler.build_system_prompt('ctx', 'persona', '')
    assert 'HOW THIS COURSE TEACHES' not in prompt


def test_teaching_notes_reach_the_composed_prompt():
    import claude_handler
    from auth import load_skin_notes
    prompt = claude_handler.build_system_prompt(
        'ctx', 'persona', load_skin_notes('csc134'))
    assert 'HOW THIS COURSE TEACHES' in prompt
    assert '-Wempty-body' in prompt


def test_csc134_persona_teaches_the_mail_run_not_pull_requests():
    """First-years submit with stage/commit/push — "the Mail Run". They are
    not put in front of a pull request in this course at all. The original
    persona claimed a fork/branch/commit/PR workflow, which would have had
    the bot coaching week-1 students through a process the course
    deliberately does not use."""
    persona = load_skin_persona('csc134')
    assert 'Mail Run' in persona
    for step in ('git add', 'git commit', 'git push'):
        assert step in persona, step
    assert 'Do not teach pull requests' in persona


def test_csc114_persona_preserves_algocratic_voice():
    """CSC 114 is a live cohort mid-pilot; the persona moved verbatim and
    must keep behaving exactly as it did before the split."""
    persona = load_skin_persona('csc114')
    assert 'AlgoCratic Futures capstone' in persona
    assert 'The Algorithm suggests' in persona
    assert 'Sacred Workflow' in persona


def test_load_skin_context_missing_header_raises(tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    with pytest.raises(FileNotFoundError):
        load_skin_context('csc114')


def test_load_skin_context_unknown_slug_raises():
    with pytest.raises(KeyError):
        load_skin_context('bogus')


def test_load_skin_context_skips_symlinks_in_corpus(tmp_path, monkeypatch):
    """A hostile symlink inside the active module must not leak host-file
    contents into Claude's system prompt."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    corpus = _window(tmp_path)
    module = corpus / 'week-02-keras-hello-world'
    secret = tmp_path / 'secret.txt'
    secret.write_text('do-not-vendor-me')
    try:
        (module / 'evil.md').symlink_to(secret)
    except (OSError, NotImplementedError) as e:
        # Windows needs Developer Mode or admin rights to create symlinks.
        pytest.skip(f'symlinks unavailable on this platform: {e}')

    out = load_skin_context('csc114')
    assert '# active body' in out
    assert 'do-not-vendor-me' not in out
    assert 'evil.md' not in out


