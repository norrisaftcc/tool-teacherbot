# tests/test_auth.py
import pytest
from pathlib import Path
from auth import authenticate_group, load_group_context, GROUPS


def test_valid_credentials():
    group = authenticate_group('group1', 'capstone2026')
    assert group is not None
    assert group['clearance'] == 'ORANGE'


def test_invalid_password():
    result = authenticate_group('group1', 'wrongpassword')
    assert result is None


def test_invalid_group():
    result = authenticate_group('group99', 'capstone2026')
    assert result is None


def test_all_five_groups_defined():
    for i in range(1, 6):
        assert f'group{i}' in GROUPS


def test_load_group_context_returns_content(tmp_path):
    import auth
    original = auth.CONTEXT_DIR
    auth.CONTEXT_DIR = tmp_path
    (tmp_path / 'group1_context.md').write_text('# Test context')
    result = load_group_context('group1')
    assert '# Test context' in result
    auth.CONTEXT_DIR = original


def test_load_group_context_raises_on_missing(tmp_path):
    import auth
    original = auth.CONTEXT_DIR
    auth.CONTEXT_DIR = tmp_path
    with pytest.raises(FileNotFoundError):
        load_group_context('group1')
    auth.CONTEXT_DIR = original


def test_login_route_success(client, tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'group1_context.md').write_text('# Group 1')
    response = client.post('/login', data={
        'group_id': 'group1',
        'password': 'capstone2026'
    }, follow_redirects=False)
    assert response.status_code == 302


def test_login_route_bad_password(client):
    response = client.post('/login', data={
        'group_id': 'group1',
        'password': 'wrong'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid' in response.data


def test_logout_clears_session(client, tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'group1_context.md').write_text('# Group 1')
    client.post('/login', data={'group_id': 'group1', 'password': 'capstone2026'})
    response = client.get('/logout', follow_redirects=False)
    assert response.status_code == 302
    # After logout, chat should redirect
    chat_response = client.get('/chat', follow_redirects=False)
    assert chat_response.status_code == 302
