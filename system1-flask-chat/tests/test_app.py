# tests/test_app.py
def test_app_creates_successfully(app):
    assert app is not None

def test_login_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200

def test_chat_redirects_when_not_logged_in(client):
    response = client.get('/chat')
    assert response.status_code == 302
