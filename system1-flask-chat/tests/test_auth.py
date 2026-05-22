# tests/test_auth.py
import pytest
from auth import authenticate_group, load_group_context, GROUPS


def test_valid_credentials():
    group = authenticate_group('csc114', '2026su')
    assert group is not None
    assert group['clearance'] == 'ORANGE'


def test_invalid_password():
    result = authenticate_group('csc114', 'wrongpassword')
    assert result is None


def test_invalid_group():
    result = authenticate_group('group99', '2026su')
    assert result is None


def test_group1_removed():
    assert 'group1' not in GROUPS


def test_csc114_present():
    assert 'csc114' in GROUPS
    assert GROUPS['csc114']['password'] == '2026su'
    assert GROUPS['csc114']['clearance'] == 'ORANGE'


def test_five_cohorts_defined():
    expected = {'csc114', 'group2', 'group3', 'group4', 'group5'}
    assert set(GROUPS.keys()) == expected


def test_load_group_context_returns_content(tmp_path):
    import auth
    original = auth.CONTEXT_DIR
    auth.CONTEXT_DIR = tmp_path
    try:
        (tmp_path / 'csc114_context.md').write_text('# Test context')
        result = load_group_context('csc114')
        assert '# Test context' in result
    finally:
        auth.CONTEXT_DIR = original


def test_load_group_context_raises_on_missing(tmp_path):
    import auth
    original = auth.CONTEXT_DIR
    auth.CONTEXT_DIR = tmp_path
    try:
        with pytest.raises(FileNotFoundError):
            load_group_context('csc114')
    finally:
        auth.CONTEXT_DIR = original


def test_login_route_success(client, tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# CSC 114')
    response = client.post('/login', data={
        'group_id': 'csc114',
        'password': '2026su',
    }, follow_redirects=False)
    assert response.status_code == 302


def test_login_route_bad_password(client):
    response = client.post('/login', data={
        'group_id': 'csc114',
        'password': 'wrong',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid' in response.data


def test_logout_clears_session(client, tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# CSC 114')
    client.post('/login', data={'group_id': 'csc114', 'password': '2026su'})
    response = client.get('/logout', follow_redirects=False)
    assert response.status_code == 302
    chat_response = client.get('/chat', follow_redirects=False)
    assert chat_response.status_code == 302
