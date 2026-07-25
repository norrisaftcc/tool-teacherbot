# tests/test_app.py
def test_app_creates_successfully(app):
    assert app is not None

def test_picker_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'CSC114' in response.data.upper()
    assert b'CSC134' in response.data.upper()

def test_skin_chat_redirects_when_not_logged_in(client):
    response = client.get('/csc114/chat')
    assert response.status_code == 302
