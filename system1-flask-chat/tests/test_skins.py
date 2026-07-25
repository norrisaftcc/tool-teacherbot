# tests/test_skins.py
"""Integration tests for the skin-per-URL contract from ADR-0001."""
import json
from unittest.mock import patch

import pytest


@pytest.fixture
def both_contexts(tmp_path, monkeypatch):
    """Mount tmp CONTEXT_DIR with headers and personas for both skins."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# csc114 header')
    (tmp_path / 'csc134_context.md').write_text('# csc134 header')
    (tmp_path / 'csc114_persona.md').write_text('# csc114 persona')
    (tmp_path / 'csc134_persona.md').write_text('# csc134 persona')
    return tmp_path


def _login(client, slug, password):
    return client.post(f'/{slug}/login', data={'password': password})


# ---- picker ---------------------------------------------------------------

def test_root_picker_lists_both_skins(client):
    r = client.get('/')
    assert r.status_code == 200
    body = r.data.decode()
    assert '/csc114/' in body
    assert '/csc134/' in body
    # Model names visible on the card so instructors can tell them apart
    assert 'claude-sonnet-4-6' in body
    assert 'claude-haiku-4-5-20251001' in body


# ---- per-skin login ------------------------------------------------------

def test_csc114_login_roundtrip_with_original_passcode(client, both_contexts):
    """CSC 114 regression: the 2026su passcode still authenticates through
    the new /csc114/login endpoint and lands on /csc114/chat."""
    r = _login(client, 'csc114', '2026su')
    assert r.status_code == 302
    assert '/csc114/chat' in r.headers['Location']

    r = client.get('/csc114/chat')
    assert r.status_code == 200


def test_csc134_login_roundtrip_with_placeholder_passcode(client, both_contexts):
    from auth import SKINS
    r = _login(client, 'csc134', SKINS['csc134']['password'])
    assert r.status_code == 302
    assert '/csc134/chat' in r.headers['Location']

    # Follow through: the chat page must actually render so a template
    # regression on the csc134 render path can't slip past.
    r = client.get('/csc134/chat')
    assert r.status_code == 200
    assert b'CSC134' in r.data.upper()


def test_login_wrong_password_flashes_and_stays(client, both_contexts):
    r = _login(client, 'csc134', 'not-the-passcode')
    assert r.status_code == 200
    assert b'Invalid' in r.data


# ---- per-skin model routing ---------------------------------------------

def _bound_arg(mock_call, name):
    """Extract a named argument regardless of positional/kwarg call style."""
    import inspect
    import claude_handler
    sig = inspect.signature(claude_handler.get_claude_response)
    bound = sig.bind(*mock_call.args, **mock_call.kwargs)
    return bound.arguments.get(name)


def test_api_chat_calls_handler_with_csc114_sonnet_model(client, both_contexts):
    _login(client, 'csc114', '2026su')
    with patch('routes.get_claude_response', return_value=('ok', 5)) as mocked:
        r = client.post(
            '/csc114/api/chat',
            json={'message': 'hi', 'history': []},
            content_type='application/json',
        )
        assert r.status_code == 200
        assert _bound_arg(mocked.call_args, 'model') == 'claude-sonnet-4-6'
        # Handler must receive the loaded context, not an empty string.
        assert _bound_arg(mocked.call_args, 'group_context')


def test_api_chat_calls_handler_with_csc134_haiku_model(client, both_contexts):
    from auth import SKINS
    _login(client, 'csc134', SKINS['csc134']['password'])
    with patch('routes.get_claude_response', return_value=('ok', 5)) as mocked:
        r = client.post(
            '/csc134/api/chat',
            json={'message': 'hi', 'history': []},
            content_type='application/json',
        )
        assert r.status_code == 200
        assert _bound_arg(mocked.call_args, 'model') == 'claude-haiku-4-5-20251001'
        assert _bound_arg(mocked.call_args, 'group_context')


@pytest.mark.parametrize('slug', ['csc114', 'csc134'])
def test_api_chat_sends_each_skins_own_persona(client, both_contexts, slug):
    """ADR-0002: the persona is per-skin. A route that dropped the kwarg
    would silently fall back to the generic persona for every cohort."""
    from auth import SKINS
    _login(client, slug, SKINS[slug]['password'])
    with patch('routes.get_claude_response', return_value=('ok', 5)) as mocked:
        client.post(
            f'/{slug}/api/chat',
            json={'message': 'hi', 'history': []},
            content_type='application/json',
        )
    assert _bound_arg(mocked.call_args, 'persona') == f'# {slug} persona'


def test_login_rejected_when_persona_file_missing(client, tmp_path, monkeypatch):
    """A missing persona must surface at login, not as a 500 on first
    message — same contract the cohort header already had."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# csc114 header')
    # no csc114_persona.md

    r = _login(client, 'csc114', '2026su')
    assert r.status_code == 200
    assert b'Persona missing' in r.data


# ---- cross-skin isolation ----------------------------------------------

def test_cross_skin_session_redirects_to_correct_skin_login(client, both_contexts):
    """Log into csc114, then hit /csc134/chat — must 302 to /csc134/
    (that skin's login), not serve the csc134 chat page."""
    _login(client, 'csc114', '2026su')
    r = client.get('/csc134/chat')
    assert r.status_code == 302
    assert '/csc134/' in r.headers['Location']
    assert 'chat' not in r.headers['Location']


def test_cross_skin_api_chat_is_gated(client, both_contexts):
    """Log into csc114, then POST /csc134/api/chat. The gate must reject
    BEFORE the handler runs (otherwise csc114's context leaks to csc134's
    model and, on a CI runner with ANTHROPIC_API_KEY set, we bill real
    money on a smoke test)."""
    _login(client, 'csc114', '2026su')
    with patch('routes.get_claude_response') as mocked:
        r = client.post(
            '/csc134/api/chat',
            json={'message': 'hi', 'history': []},
            content_type='application/json',
        )
    assert r.status_code == 401
    mocked.assert_not_called()


def test_second_skin_login_replaces_first(client, both_contexts):
    """Logging into csc134 while a csc114 session is live overwrites it —
    single session slot, per ADR."""
    from auth import SKINS
    _login(client, 'csc114', '2026su')
    _login(client, 'csc134', SKINS['csc134']['password'])
    with client.session_transaction() as s:
        assert s['skin'] == 'csc134'


def test_login_cookie_stays_under_browser_limit_with_large_corpus(client, tmp_path, monkeypatch):
    """Regression: an earlier revision stashed load_skin_context() into
    session['skin_context']. With the real csc114 corpus (~40KB) that
    exceeded the 4093-byte signed-cookie limit — browsers silently
    dropped the cookie, so /csc114/chat re-redirected to login (loop).
    The session must not carry the full corpus."""
    import auth
    from auth import SKINS
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# csc114 header')
    (tmp_path / 'csc114_persona.md').write_text('# csc114 persona')
    module = tmp_path / 'csc114' / SKINS['csc114']['active_module']
    module.mkdir(parents=True)
    for i in range(30):
        (module / f'lesson-{i:02d}.md').write_text('x' * 2000)  # ~60KB in-window

    r = client.post('/csc114/login', data={'password': '2026su'})
    assert r.status_code == 302
    cookies = r.headers.getlist('Set-Cookie')
    for c in cookies:
        assert len(c) < 4093, f'Set-Cookie exceeds browser limit: {len(c)} bytes'


# CSC 134 manifest shape assertions live in tests/test_sync_course_corpus.py
# alongside the sync-script tests — a manifest is a sync-script contract,
# not a skin contract. Deduplicated per review finding f12.
