# System 1: Flask Chat Interface — Implementation Plan

> **HISTORICAL — do not act on this file.** The May 2026 build plan for the MVP:
> five hardcoded group credentials, SQLite, Flask-Login, no corpus window, no
> migrations. It targets a design that ADR-0001, ADR-0002 and ADR-0006 have since
> replaced, and it points at `SYSTEM1_CLAUDE.md`, which now lives in
> `docs/historical/`. Kept as a paper trail. For what is actually true, read
> `docs/adr/`, `docs/registry/KEEP.md`, and `system1-flask-chat/DEPLOY.md`.
>
> *This was written for task-by-task execution by an agent; it records how the
> work was sequenced, not how to sequence work now.*

**Goal:** Build a group-authenticated Flask web chat that injects per-group project context into Claude responses and logs all conversations to SQLite.

**Architecture:** Structured Flask app with strict layer separation — `models.py` owns DB, `auth.py` and `claude_handler.py` own business logic, `app.py` owns routes, templates/static own UI. 5 hardcoded group credentials for alpha; SQLite locally with SQLAlchemy so Render/PostgreSQL swap is a one-line config change.

**Tech Stack:** Python 3.11+, Flask 3.x, Flask-Login, Flask-SQLAlchemy, Anthropic SDK (`anthropic`), python-dotenv, pytest, gunicorn (Render only)

---

## Pre-Task: Read These First

- `docs/historical/plans/2026-05-12-system1-design.md` — approved design (routes, models, error handling)
- `docs/design/design-guidelines.md` — UI spec (check before writing any CSS/HTML; designer may have updated it)
- `SYSTEM1_CLAUDE.md` — additional context on pedagogical prompt structure

---

### Task 1: Project Scaffold

**Files:**
- Create: `system1-flask-chat/requirements.txt`
- Create: `system1-flask-chat/.env.example`
- Create: `system1-flask-chat/tests/__init__.py`
- Create: `system1-flask-chat/tests/conftest.py`

**Step 1: Create directory structure**

```bash
mkdir -p system1-flask-chat/tests
mkdir -p system1-flask-chat/templates
mkdir -p system1-flask-chat/static/css
mkdir -p system1-flask-chat/static/js
mkdir -p system1-flask-chat/context
touch system1-flask-chat/tests/__init__.py
```

**Step 2: Create `requirements.txt`**

```
flask==3.0.0
flask-login==0.6.3
flask-sqlalchemy==3.1.1
anthropic==0.18.0
python-dotenv==1.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
pytest==8.0.0
pytest-flask==1.3.0
```

**Step 3: Create `.env.example`**

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
FLASK_SECRET_KEY=change-me-in-production
ADMIN_PASSWORD=admin
DATABASE_URL=sqlite:///ta_system.db
```

**Step 4: Create `tests/conftest.py`**

```python
import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret',
        'ADMIN_PASSWORD': 'testadmin',
        'WTF_CSRF_ENABLED': False,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
```

**Step 5: Create virtual environment and install deps**

```bash
cd system1-flask-chat
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Step 6: Verify install**

```bash
python -c "import flask, flask_login, flask_sqlalchemy, anthropic; print('OK')"
```
Expected: `OK`

**Step 7: Commit**

```bash
git add system1-flask-chat/
git commit -m "feat(system1): project scaffold, requirements, test config"
```

---

### Task 2: Database Models

**Files:**
- Create: `system1-flask-chat/models.py`
- Create: `system1-flask-chat/tests/test_models.py`

**Step 1: Write failing tests**

```python
# tests/test_models.py
import pytest
from models import Group, Conversation, Message

def test_group_defaults(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='group1', clearance_level='ORANGE')
        db.session.add(g)
        db.session.commit()
        assert g.token_budget == 100000
        assert g.tokens_used == 0

def test_conversation_linked_to_group(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='group2', clearance_level='YELLOW')
        db.session.add(g)
        db.session.commit()
        c = Conversation(group_id=g.id)
        db.session.add(c)
        db.session.commit()
        assert c.group_id == g.id

def test_message_linked_to_conversation(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='group3', clearance_level='ORANGE')
        db.session.add(g)
        db.session.commit()
        c = Conversation(group_id=g.id)
        db.session.add(c)
        db.session.commit()
        m = Message(conversation_id=c.id, role='user', content='Hello', tokens_used=5)
        db.session.add(m)
        db.session.commit()
        assert m.role == 'user'
        assert m.tokens_used == 5

def test_group_increment_tokens(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='group4', clearance_level='ORANGE')
        db.session.add(g)
        db.session.commit()
        g.increment_tokens(500)
        db.session.commit()
        assert g.tokens_used == 500
        assert g.tokens_remaining == 99500
```

**Step 2: Run tests to verify they fail**

```bash
cd system1-flask-chat
source venv/bin/activate
pytest tests/test_models.py -v
```
Expected: ImportError or similar — `models.py` doesn't exist yet.

**Step 3: Create `models.py`**

```python
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    clearance_level = db.Column(db.String(20), nullable=False)
    token_budget = db.Column(db.Integer, default=100000, nullable=False)
    tokens_used = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    conversations = db.relationship('Conversation', backref='group', lazy=True)

    @property
    def tokens_remaining(self):
        return self.token_budget - self.tokens_used

    def increment_tokens(self, count):
        self.tokens_used += count


class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    messages = db.relationship('Message', backref='conversation', lazy=True)


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)   # 'user' | 'assistant'
    content = db.Column(db.Text, nullable=False)
    tokens_used = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
```

**Step 4: Run tests — expect pass**

```bash
pytest tests/test_models.py -v
```
Expected: 4 passed

**Step 5: Commit**

```bash
git add system1-flask-chat/models.py system1-flask-chat/tests/test_models.py
git commit -m "feat(system1): database models with token tracking"
```

---

### Task 3: App Factory

**Files:**
- Create: `system1-flask-chat/app.py`
- Create: `system1-flask-chat/tests/test_app.py`

**Step 1: Write failing test**

```python
# tests/test_app.py
def test_app_creates_successfully(app):
    assert app is not None

def test_login_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200

def test_chat_redirects_when_not_logged_in(client):
    response = client.get('/chat')
    assert response.status_code == 302
    assert '/login' in response.headers['Location'] or '/' in response.headers['Location']
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_app.py -v
```
Expected: ImportError — `app.py` doesn't exist yet.

**Step 3: Create `app.py`**

```python
import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from dotenv import load_dotenv
from models import db

load_dotenv()

login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__)

    # Config
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ta_system.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD', 'admin')

    if test_config:
        app.config.update(test_config)

    # Extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Blueprints (imported here to avoid circular imports)
    from routes import main
    app.register_blueprint(main)

    # Create tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

**Step 4: Create `routes.py` stub** (enough to make the test pass — routes will be filled in Tasks 4-6)

```python
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('login.html')

@main.route('/chat')
@login_required
def chat():
    return render_template('chat.html')
```

**Step 5: Create minimal `templates/login.html` and `templates/chat.html`** (content expanded in Task 8)

```html
<!-- templates/login.html -->
<!DOCTYPE html><html><body><h1>Login</h1></body></html>
```

```html
<!-- templates/chat.html -->
<!DOCTYPE html><html><body><h1>Chat</h1></body></html>
```

**Step 6: Run tests — expect pass**

```bash
pytest tests/test_app.py -v
```
Expected: 3 passed

**Step 7: Commit**

```bash
git add system1-flask-chat/app.py system1-flask-chat/routes.py \
        system1-flask-chat/templates/
git commit -m "feat(system1): app factory and route stubs"
```

---

### Task 4: Auth Module

**Files:**
- Create: `system1-flask-chat/auth.py`
- Modify: `system1-flask-chat/routes.py`
- Create: `system1-flask-chat/tests/test_auth.py`

**Step 1: Write failing tests**

```python
# tests/test_auth.py
from auth import authenticate_group, GROUPS

def test_valid_credentials():
    group = authenticate_group('group1', 'capstone2026')
    assert group is not None
    assert group['clearance'] == 'ORANGE'

def test_invalid_password():
    group = authenticate_group('group1', 'wrongpassword')
    assert group is None

def test_invalid_group():
    group = authenticate_group('group99', 'capstone2026')
    assert group is None

def test_login_route_success(client):
    response = client.post('/login', data={
        'group_id': 'group1',
        'password': 'capstone2026'
    }, follow_redirects=False)
    assert response.status_code == 302

def test_login_route_failure(client):
    response = client.post('/login', data={
        'group_id': 'group1',
        'password': 'wrong'
    }, follow_redirects=True)
    assert b'Invalid' in response.data or response.status_code == 200

def test_logout_clears_session(client):
    # Login first
    client.post('/login', data={'group_id': 'group1', 'password': 'capstone2026'})
    response = client.get('/logout', follow_redirects=False)
    assert response.status_code == 302
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_auth.py -v
```
Expected: ImportError — `auth.py` doesn't exist.

**Step 3: Create `auth.py`**

```python
import os
from pathlib import Path

# Alpha: hardcoded credentials. Replace with DB-backed auth post-alpha.
GROUPS = {
    'group1': {'password': 'capstone2026', 'clearance': 'ORANGE'},
    'group2': {'password': 'dataman2026',  'clearance': 'YELLOW'},
    'group3': {'password': 'finaid2026',   'clearance': 'ORANGE'},
    'group4': {'password': 'health2026',   'clearance': 'YELLOW'},
    'group5': {'password': 'sched2026',    'clearance': 'ORANGE'},
}

CONTEXT_DIR = Path(__file__).parent / 'context'


def authenticate_group(group_id: str, password: str) -> dict | None:
    """Return group dict if credentials valid, else None."""
    group = GROUPS.get(group_id)
    if group and group['password'] == password:
        return group
    return None


def load_group_context(group_id: str) -> str:
    """Load group context from markdown file. Raises FileNotFoundError if missing."""
    context_file = CONTEXT_DIR / f'{group_id}_context.md'
    if not context_file.exists():
        raise FileNotFoundError(f'No context file for {group_id}. '
                                f'Create context/{group_id}_context.md first.')
    return context_file.read_text()
```

**Step 4: Update `routes.py` to add login/logout**

Add these imports and routes (keep existing stubs):

```python
from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import login_required, login_user, logout_user, current_user
from auth import authenticate_group, load_group_context
from models import db, Group

# ... existing blueprint definition ...

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        group_id = request.form.get('group_id', '').strip()
        password = request.form.get('password', '').strip()
        group_data = authenticate_group(group_id, password)
        if not group_data:
            flash('Invalid group ID or password.')
            return render_template('login.html'), 200
        try:
            context = load_group_context(group_id)
        except FileNotFoundError as e:
            flash(str(e))
            return render_template('login.html'), 200
        session['group_id'] = group_id
        session['group_context'] = context
        session['clearance'] = group_data['clearance']
        # Ensure Group row exists in DB
        group = Group.query.filter_by(name=group_id).first()
        if not group:
            group = Group(name=group_id, clearance_level=group_data['clearance'])
            db.session.add(group)
            db.session.commit()
        return redirect(url_for('main.chat'))
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
```

**Note on Flask-Login:** For this alpha, `login_required` uses a lightweight session check rather than a full UserMixin model — the session `group_id` key acts as the auth token. If Flask-Login's `login_user` requires a UserMixin, use a simple session check decorator instead:

```python
# Add to routes.py — use @group_login_required instead of @login_required
from functools import wraps

def group_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'group_id' not in session:
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated
```

**Step 5: Run tests — expect pass**

```bash
pytest tests/test_auth.py -v
```
Expected: 6 passed

**Step 6: Commit**

```bash
git add system1-flask-chat/auth.py system1-flask-chat/routes.py \
        system1-flask-chat/tests/test_auth.py
git commit -m "feat(system1): auth module with group credentials and context loading"
```

---

### Task 5: Claude Handler

**Files:**
- Create: `system1-flask-chat/claude_handler.py`
- Create: `system1-flask-chat/tests/test_claude_handler.py`

**Step 1: Write failing tests** (no real API calls — mock the Anthropic client)

```python
# tests/test_claude_handler.py
from unittest.mock import MagicMock, patch
from claude_handler import build_system_prompt, get_claude_response

SAMPLE_CONTEXT = """
# Group 1 Context
## Project Overview
- Product: DataMan Math Platform
- Tech Stack: Flask, SQLite, React
"""

def test_system_prompt_contains_context():
    prompt = build_system_prompt(SAMPLE_CONTEXT)
    assert 'DataMan' in prompt
    assert 'PEDAGOGICAL' in prompt.upper() or 'teaching' in prompt.lower()

def test_system_prompt_contains_guardrails():
    prompt = build_system_prompt(SAMPLE_CONTEXT)
    assert 'Sacred Workflow' in prompt or 'direct solution' in prompt.lower()

def test_get_claude_response_returns_content():
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text='Test response')]
    mock_message.usage.input_tokens = 100
    mock_message.usage.output_tokens = 50
    mock_client.messages.create.return_value = mock_message

    with patch('claude_handler.client', mock_client):
        response, tokens = get_claude_response(SAMPLE_CONTEXT, [], 'Hello')
        assert response == 'Test response'
        assert tokens == 150

def test_get_claude_response_formats_history():
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text='Reply')]
    mock_message.usage.input_tokens = 10
    mock_message.usage.output_tokens = 5
    mock_client.messages.create.return_value = mock_message

    history = [
        {'role': 'user', 'content': 'First message'},
        {'role': 'assistant', 'content': 'First reply'},
    ]
    with patch('claude_handler.client', mock_client):
        get_claude_response(SAMPLE_CONTEXT, history, 'Second message')
        call_args = mock_client.messages.create.call_args
        messages = call_args.kwargs['messages']
        # Should include history + new user message
        assert len(messages) == 3
        assert messages[-1]['role'] == 'user'
        assert messages[-1]['content'] == 'Second message'
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_claude_handler.py -v
```
Expected: ImportError — `claude_handler.py` doesn't exist.

**Step 3: Create `claude_handler.py`**

```python
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

MODEL = 'claude-sonnet-4-6'
MAX_TOKENS = 1024


def build_system_prompt(group_context: str) -> str:
    return f"""You are an AI teaching assistant for the AlgoCratic Futures capstone course.

CURRENT GROUP CONTEXT:
{group_context}

PEDAGOGICAL RULES:
1. Never provide direct solutions — guide students through iteration
2. Ask students to explain their attempt before you help
3. Ask clarifying questions before answering
4. Emphasize the Sacred Workflow: Issue → Branch → PR → Review → Merge
5. Reference the group's specific project context when relevant
6. Celebrate iteration and learning velocity, not just correct answers

VOCABULARY:
- Say "growth opportunity" not "error"
- Say "suboptimal" not "wrong"
- Say "The Algorithm suggests" not "You should"

RESPONSE STYLE:
- Technical but encouraging
- Light AlgoCratic voice (5% seasoning — don't overdo it)
- Competence and clarity over entertainment
"""


def get_claude_response(
    group_context: str,
    history: list[dict],
    user_message: str,
) -> tuple[str, int]:
    """
    Call Claude with context and conversation history.

    Args:
        group_context: The group's project context markdown string
        history: List of {'role': 'user'|'assistant', 'content': str} dicts
        user_message: The new message from the student

    Returns:
        (response_text, total_tokens_used)
    """
    messages = history + [{'role': 'user', 'content': user_message}]

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=build_system_prompt(group_context),
        messages=messages,
    )

    text = response.content[0].text
    tokens = response.usage.input_tokens + response.usage.output_tokens
    return text, tokens
```

**Step 4: Run tests — expect pass**

```bash
pytest tests/test_claude_handler.py -v
```
Expected: 4 passed

**Step 5: Commit**

```bash
git add system1-flask-chat/claude_handler.py system1-flask-chat/tests/test_claude_handler.py
git commit -m "feat(system1): Claude handler with pedagogical system prompt"
```

---

### Task 6: Chat and Admin Routes

**Files:**
- Modify: `system1-flask-chat/routes.py`
- Create: `system1-flask-chat/tests/test_routes.py`
- Create: `system1-flask-chat/context/group_1_context.md` (and groups 2-5)

**Step 1: Create context files** (stubs — instructor fills in details)

```bash
for i in 1 2 3 4 5; do cat > system1-flask-chat/context/group_${i}_context.md << EOF
# Group $i Context

## Project Overview
- Product: [INSTRUCTOR: fill in]
- Tech Stack: [INSTRUCTOR: fill in]
- Current Sprint: Sprint 1

## Team Members
- [INSTRUCTOR: fill in]

## Current Sprint Focus
[INSTRUCTOR: fill in]

## Known Issues
- None yet

## Clearance Level
ORANGE
EOF
done
```

**Step 2: Write failing tests**

```python
# tests/test_routes.py
import json
from unittest.mock import patch

def login(client, group_id='group1', password='capstone2026'):
    return client.post('/login', data={'group_id': group_id, 'password': password})

def test_chat_page_requires_login(client):
    response = client.get('/chat')
    assert response.status_code == 302

def test_chat_page_loads_after_login(client, tmp_path, monkeypatch):
    # Point context dir to tmp so no real file needed
    monkeypatch.setattr('auth.CONTEXT_DIR', tmp_path)
    (tmp_path / 'group1_context.md').write_text('# Test context')
    login(client)
    response = client.get('/chat')
    assert response.status_code == 200

def test_api_chat_requires_login(client):
    response = client.post('/api/chat', json={'message': 'hi'})
    assert response.status_code == 302

def test_api_chat_returns_json(client, tmp_path, monkeypatch):
    monkeypatch.setattr('auth.CONTEXT_DIR', tmp_path)
    (tmp_path / 'group1_context.md').write_text('# Test context')
    login(client)
    with patch('routes.get_claude_response', return_value=('Claude says hi', 100)):
        response = client.post('/api/chat', json={'message': 'Hello', 'history': []})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'response' in data
        assert 'tokens_remaining' in data

def test_admin_requires_password(client):
    response = client.get('/admin')
    # Should either redirect or show password prompt
    assert response.status_code in (200, 302)

def test_admin_accessible_with_password(client):
    response = client.get('/admin?password=testadmin')
    assert response.status_code == 200
```

**Step 3: Run tests to verify they fail**

```bash
pytest tests/test_routes.py -v
```
Expected: failures — routes not fully implemented yet.

**Step 4: Complete `routes.py`**

Add these routes (replacing the stubs from Task 3):

```python
@main.route('/chat')
@group_login_required
def chat():
    return render_template('chat.html',
                           group_id=session['group_id'],
                           clearance=session.get('clearance', ''))

@main.route('/api/chat', methods=['POST'])
@group_login_required
def api_chat():
    from claude_handler import get_claude_response
    data = request.get_json()
    user_message = data.get('message', '').strip()
    history = data.get('history', [])

    if not user_message:
        return {'error': 'Empty message'}, 400

    group = Group.query.filter_by(name=session['group_id']).first()
    if group and group.tokens_remaining <= 0:
        return {'error': 'Token budget exhausted. Contact your instructor.'}, 403

    try:
        response_text, tokens_used = get_claude_response(
            session['group_context'], history, user_message
        )
    except Exception as e:
        return {'error': f'Claude API error: {str(e)}'}, 502

    # Log to DB
    try:
        conv = Conversation.query.filter_by(
            group_id=group.id
        ).order_by(Conversation.started_at.desc()).first()
        if not conv or len(history) == 0:
            conv = Conversation(group_id=group.id)
            db.session.add(conv)
            db.session.flush()

        db.session.add(Message(conversation_id=conv.id, role='user',
                               content=user_message, tokens_used=0))
        db.session.add(Message(conversation_id=conv.id, role='assistant',
                               content=response_text, tokens_used=tokens_used))
        group.increment_tokens(tokens_used)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Log but don't block the response
        print(f'DB write failed: {e}')

    return {
        'response': response_text,
        'tokens_remaining': group.tokens_remaining if group else None,
    }

@main.route('/admin')
def admin():
    # Simple password-in-query-string for alpha demo
    password = request.args.get('password', '')
    from flask import current_app
    if password != current_app.config.get('ADMIN_PASSWORD', ''):
        return render_template('admin_login.html'), 200
    groups = Group.query.all()
    conversations = Conversation.query.order_by(Conversation.started_at.desc()).limit(50).all()
    return render_template('admin.html', groups=groups, conversations=conversations)
```

Also import `Conversation` at the top of `routes.py`:
```python
from models import db, Group, Conversation, Message
```

**Step 5: Run tests — expect pass**

```bash
pytest tests/test_routes.py -v
```
Expected: 6 passed

**Step 6: Commit**

```bash
git add system1-flask-chat/routes.py system1-flask-chat/context/ \
        system1-flask-chat/tests/test_routes.py
git commit -m "feat(system1): chat API and admin routes with conversation logging"
```

---

### Task 7: Templates and Static Files

**Files:**
- Modify: `system1-flask-chat/templates/login.html`
- Modify: `system1-flask-chat/templates/chat.html`
- Create: `system1-flask-chat/templates/admin.html`
- Create: `system1-flask-chat/templates/admin_login.html`
- Create: `system1-flask-chat/static/css/terminal.css`
- Create: `system1-flask-chat/static/js/chat.js`

> **STOP:** Before writing any HTML/CSS, re-read `docs/design/design-guidelines.md`.
> If the designer has populated color tokens, typography, and component specs — implement from those.
> If it's still mostly TBD stubs — implement a functional placeholder using sensible defaults
> (dark bg `#0d0d0d`, green text `#00ff41`, IBM Plex Mono) and note it needs design review.

**Step 1: Create `static/css/terminal.css`**

Implement CSS custom properties from the design guidelines. Minimum:

```css
/* terminal.css — AlgoCratic TA System 1 */
/* Source of truth: docs/design/design-guidelines.md */

:root {
  --color-bg: #0d0d0d;
  --color-surface: #1a1a1a;
  --color-primary: #00ff41;
  --color-secondary: #888;
  --color-border: #333;
  --color-error: #ff4444;
  --font-mono: 'IBM Plex Mono', 'Courier New', monospace;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--color-bg);
  color: var(--color-primary);
  font-family: var(--font-mono);
  font-size: 14px;
  line-height: 1.6;
}

/* Add component styles per design-guidelines.md spec */
```

**Step 2: Create `static/js/chat.js`**

```javascript
// chat.js — handles message send/receive without page reload
const form = document.getElementById('chat-form');
const input = document.getElementById('message-input');
const log = document.getElementById('chat-log');
let history = [];

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  appendMessage('user', message);
  history.push({ role: 'user', content: message });
  input.value = '';
  input.disabled = true;

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history: history.slice(0, -1) }),
    });
    const data = await res.json();

    if (!res.ok) {
      appendMessage('error', data.error || 'Something went wrong.');
    } else {
      appendMessage('assistant', data.response);
      history.push({ role: 'assistant', content: data.response });
      updateTokenCounter(data.tokens_remaining);
    }
  } catch (err) {
    appendMessage('error', 'Network error. Try again.');
  } finally {
    input.disabled = false;
    input.focus();
  }
});

function appendMessage(role, content) {
  const div = document.createElement('div');
  div.className = `message message--${role}`;
  div.textContent = content;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

function updateTokenCounter(remaining) {
  const el = document.getElementById('tokens-remaining');
  if (el && remaining !== null) el.textContent = remaining.toLocaleString();
}
```

**Step 3: Build the templates** using the CSS classes above. Key requirements:
- `login.html`: group_id input, password input, submit button, flash message display
- `chat.html`: `#chat-log`, `#chat-form`, `#message-input`, `#tokens-remaining`, loads `chat.js`
- `admin.html`: table of groups (name, clearance, tokens used/budget), recent conversations list
- `admin_login.html`: simple form with password field that POSTs to `/admin?password=X`

**Step 4: Smoke test in browser**

```bash
cd system1-flask-chat
cp .env.example .env
# Edit .env to add real ANTHROPIC_API_KEY
source venv/bin/activate
flask run
```

Navigate to `http://localhost:5000`, log in as `group1` / `capstone2026`, send a message.

**Step 5: Commit**

```bash
git add system1-flask-chat/templates/ system1-flask-chat/static/
git commit -m "feat(system1): templates and terminal UI — pending design review"
```

---

### Task 8: Full Test Suite Pass

**Step 1: Run all tests**

```bash
cd system1-flask-chat
pytest tests/ -v
```
Expected: All pass.

**Step 2: Fix any failures before continuing**

**Step 3: Commit if any fixes were made**

```bash
git add -p  # stage only intentional changes
git commit -m "fix(system1): test suite cleanup"
```

---

### Task 9: Render Deployment (After MVP Stable)

> Run this task only after local MVP is working and signed off.

**Files:**
- Create: `system1-flask-chat/render.yaml`

**Step 1: Create `render.yaml`**

```yaml
services:
  - type: web
    name: algocratic-ta-system1
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:create_app()
    envVars:
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: FLASK_SECRET_KEY
        sync: false
      - key: ADMIN_PASSWORD
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: algocratic-ta-db
          property: connectionString

databases:
  - name: algocratic-ta-db
    databaseName: ta_system
    user: ta_admin
```

**Step 2: Switch DATABASE_URL to PostgreSQL**

On Render, `DATABASE_URL` is auto-set by the database block above. No code changes needed — SQLAlchemy handles it.

**Step 3: Deploy**

```bash
git add system1-flask-chat/render.yaml
git commit -m "feat(system1): Render deployment config"
git push origin main
```

Then connect the repo to Render dashboard → New Web Service → point to `system1-flask-chat/`.

**Step 4: Smoke test on Render URL**

- Login as group1
- Send a message
- Check admin dashboard

---

## Running the Full Test Suite

```bash
cd system1-flask-chat
source venv/bin/activate
pytest tests/ -v --tb=short
```

All tests should pass before any PR or deploy.
