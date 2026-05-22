# tests/test_routes.py
import json
from unittest.mock import patch


def login(client, group_id='csc114', password='2026su'):
    # Callers must monkeypatch auth.CONTEXT_DIR before calling login()
    # (or accept the FileNotFoundError if no fixture file exists).
    return client.post('/login', data={'group_id': group_id, 'password': password})


def test_chat_page_requires_login(client):
    response = client.get('/chat')
    assert response.status_code == 302


def test_chat_page_loads_after_login(client, tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# Test context')
    login(client)
    response = client.get('/chat')
    assert response.status_code == 200


def test_api_chat_requires_login(client):
    response = client.post('/api/chat', json={'message': 'hi', 'history': []})
    assert response.status_code == 302


def test_api_chat_returns_json(client, tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# Test context')
    login(client)
    with patch('routes.get_claude_response', return_value=('Claude says hi', 100)):
        response = client.post('/api/chat',
                               json={'message': 'Hello', 'history': []},
                               content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'response' in data
        assert 'tokens_remaining' in data


def test_api_chat_returns_error_on_api_failure(client, tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# Test context')
    login(client)
    with patch('routes.get_claude_response', side_effect=RuntimeError('API down')):
        response = client.post('/api/chat',
                               json={'message': 'Hello', 'history': []},
                               content_type='application/json')
        assert response.status_code == 502
        data = json.loads(response.data)
        assert 'error' in data


def test_api_chat_blocks_when_budget_exhausted(client, tmp_path, monkeypatch):
    import auth
    from models import db, Group
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# Test context')
    login(client)
    # Exhaust the budget
    with client.application.app_context():
        group = Group.query.filter_by(name='csc114').first()
        if group:
            group.tokens_used = group.token_budget
            db.session.commit()
    response = client.post('/api/chat',
                           json={'message': 'Hello', 'history': []},
                           content_type='application/json')
    assert response.status_code == 403


def test_admin_shows_password_prompt_without_password(client):
    response = client.get('/admin')
    assert response.status_code == 200


def test_admin_accessible_with_correct_password(client):
    response = client.get('/admin?password=testadmin')
    assert response.status_code == 200
