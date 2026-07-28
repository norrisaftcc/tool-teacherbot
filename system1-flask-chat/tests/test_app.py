# tests/test_app.py
import pytest

from app import create_app


def test_app_creates_successfully(app):
    assert app is not None


# ---- fail closed on missing secrets ---------------------------------------
#
# Both are sync:false in render.yaml, so an operator sets them by hand and
# can forget. The old fallbacks ('dev-secret', 'admin') made that forgetting
# silent: the service came up healthy and signed session cookies with a
# value published in this public repo.

@pytest.mark.parametrize('missing_var', ['FLASK_SECRET_KEY', 'ADMIN_PASSWORD'])
def test_create_app_refuses_to_start_without_a_secret(monkeypatch, missing_var):
    monkeypatch.setenv('FLASK_SECRET_KEY', 'set')
    monkeypatch.setenv('ADMIN_PASSWORD', 'set')
    monkeypatch.delenv(missing_var, raising=False)

    with pytest.raises(RuntimeError) as excinfo:
        create_app()

    # The operator must be able to act on this without reading app.py.
    assert missing_var in str(excinfo.value)


def test_create_app_does_not_fall_back_to_the_published_defaults(monkeypatch):
    """Regression: 'dev-secret' and 'admin' must never be reachable."""
    monkeypatch.delenv('FLASK_SECRET_KEY', raising=False)
    monkeypatch.delenv('ADMIN_PASSWORD', raising=False)

    with pytest.raises(RuntimeError):
        create_app()

def test_picker_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'CSC114' in response.data.upper()
    assert b'CSC134' in response.data.upper()

def test_skin_chat_redirects_when_not_logged_in(client):
    response = client.get('/csc114/chat')
    assert response.status_code == 302
