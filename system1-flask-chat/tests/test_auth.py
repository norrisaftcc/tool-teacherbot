# tests/test_auth.py
import pytest
from auth import (
    SKINS,
    active_module,
    authenticate_skin,
    load_skin_context,
    load_skin_persona,
)


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


