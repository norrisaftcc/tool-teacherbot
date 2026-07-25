# tests/test_skins.py
"""Integration tests for the skin-per-URL contract from ADR-0001."""
import json
from unittest.mock import patch

import pytest


@pytest.fixture
def both_contexts(tmp_path, monkeypatch):
    """Mount tmp CONTEXT_DIR with headers for both skins."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# csc114 header')
    (tmp_path / 'csc134_context.md').write_text('# csc134 header')
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


def test_login_wrong_password_flashes_and_stays(client, both_contexts):
    r = _login(client, 'csc134', 'not-the-passcode')
    assert r.status_code == 200
    assert b'Invalid' in r.data


# ---- per-skin model routing ---------------------------------------------

def test_api_chat_calls_handler_with_csc114_sonnet_model(client, both_contexts):
    _login(client, 'csc114', '2026su')
    with patch('routes.get_claude_response', return_value=('ok', 5)) as mocked:
        r = client.post(
            '/csc114/api/chat',
            json={'message': 'hi', 'history': []},
            content_type='application/json',
        )
        assert r.status_code == 200
        _, kwargs = mocked.call_args
        assert kwargs.get('model') == 'claude-sonnet-4-6'


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
        _, kwargs = mocked.call_args
        assert kwargs.get('model') == 'claude-haiku-4-5-20251001'


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
    _login(client, 'csc114', '2026su')
    r = client.post(
        '/csc134/api/chat',
        json={'message': 'hi', 'history': []},
        content_type='application/json',
    )
    # api gate must not serve the response — redirect is fine, so is 401/403.
    assert r.status_code in (302, 401, 403)


def test_second_skin_login_replaces_first(client, both_contexts):
    """Logging into csc134 while a csc114 session is live overwrites it —
    single session slot, per ADR."""
    from auth import SKINS
    _login(client, 'csc114', '2026su')
    _login(client, 'csc134', SKINS['csc134']['password'])
    with client.session_transaction() as s:
        assert s['skin'] == 'csc134'


# ---- CSC 134 manifest shape --------------------------------------------

def test_csc134_manifest_shape():
    import yaml
    from pathlib import Path
    manifest_path = Path(__file__).resolve().parents[2] / 'scripts' / 'csc134_manifest.yaml'
    data = yaml.safe_load(manifest_path.read_text())
    assert 'course-csc134-template' in data['upstream']
    assert data['ref'] == 'main'
    assert data['target'] == 'system1-flask-chat/context/csc134'
    assert isinstance(data['paths'], list) and data['paths']
    assert data['strip_prefix'].endswith('/')
