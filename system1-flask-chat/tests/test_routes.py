# tests/test_routes.py
import json
from unittest.mock import patch

import pytest


@pytest.fixture
def csc114_ctx(tmp_path, monkeypatch):
    """Point auth.CONTEXT_DIR at a tmp dir with a minimal csc114 header
    and persona — login validates both."""
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# csc114 test context')
    (tmp_path / 'csc114_persona.md').write_text('# csc114 test persona')
    return tmp_path


def login_csc114(client):
    return client.post('/csc114/login', data={'password': '2026su'})


# ---- gating ---------------------------------------------------------------

def test_chat_page_requires_login(client):
    response = client.get('/csc114/chat')
    assert response.status_code == 302
    assert '/csc114/' in response.headers['Location']


def test_api_chat_requires_login(client):
    response = client.post('/csc114/api/chat', json={'message': 'hi', 'history': []})
    assert response.status_code == 401
    assert b'error' in response.data


# ---- happy path -----------------------------------------------------------

def test_chat_page_loads_after_login(client, csc114_ctx):
    login_csc114(client)
    response = client.get('/csc114/chat')
    assert response.status_code == 200
    assert b'CSC114' in response.data.upper()


def test_api_chat_returns_json(client, csc114_ctx):
    login_csc114(client)
    with patch('routes.get_claude_response', return_value=('Claude says hi', 100)):
        response = client.post(
            '/csc114/api/chat',
            json={'message': 'Hello', 'history': []},
            content_type='application/json',
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['response'] == 'Claude says hi'
        assert 'tokens_remaining' in data


def test_api_chat_returns_error_on_api_failure(client, csc114_ctx):
    login_csc114(client)
    with patch('routes.get_claude_response', side_effect=RuntimeError('API down')):
        response = client.post(
            '/csc114/api/chat',
            json={'message': 'Hello', 'history': []},
            content_type='application/json',
        )
        assert response.status_code == 502
        assert 'error' in json.loads(response.data)


def test_api_chat_blocks_when_budget_exhausted(client, csc114_ctx):
    from models import db, Group

    login_csc114(client)
    with client.application.app_context():
        group = Group.query.filter_by(name='csc114').first()
        assert group is not None, 'login must have created a Group row'
        group.tokens_used = group.token_budget
        db.session.commit()

    response = client.post(
        '/csc114/api/chat',
        json={'message': 'Hello', 'history': []},
        content_type='application/json',
    )
    assert response.status_code == 403


# ---- admin ----------------------------------------------------------------

def test_admin_shows_password_prompt_without_password(client):
    response = client.get('/csc114/admin')
    assert response.status_code == 200
    assert b'INSTRUCTOR' in response.data.upper()


def test_admin_accessible_with_correct_password(client):
    response = client.get('/csc114/admin?password=testadmin')
    assert response.status_code == 200
