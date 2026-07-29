> **HISTORICAL — do not act on this file.** It describes a project shape
> (five capstone groups, two parallel systems) that the code stopped
> matching in July 2026. Kept as a paper trail. For what is actually
> true, read `docs/adr/`, `docs/registry/KEEP.md`, and
> `system1-flask-chat/DEPLOY.md`.

# CLAUDE.md - System 1: Flask Chat Interface

**Your Role**: Build the Flask web application for authenticated, context-aware Claude conversations.

**Your Workspace**: `/ta-systems-alpha/system1-flask-chat/`

**Coordination**: Instance B is building System 2 in `/system2-code-distribution/`. You coordinate on files in `/shared/`.

---

## Quick Start

```bash
# See what needs to be built
cat /home/claude/TA_SYSTEMS_PARALLEL_PLAN.md | grep "SYSTEM 1"

# Check your timeline
# Hours 0-4: Core Flask + Claude API
# Hours 4-8: Database + logging
# Hours 8-12: Admin dashboard + context loading
# Hours 12-16: Render deployment
# Hours 16-20: Polish + docs
```

---

## What You're Building

A Flask web application that provides:
- **Student Authentication**: Group-based login (group1, group2, etc.)
- **Context-Aware Conversations**: Each group gets their own project context injected into Claude
- **Conversation Logging**: All messages stored in database with timestamps
- **Token Tracking**: Per-group budget and usage monitoring
- **Admin Dashboard**: Instructor can view all conversations and usage
- **AlgoCratic Aesthetic**: Terminal-style UI with IBM Plex Mono, green text on dark background

---

## Tech Stack

```
Flask 3.x
├── Flask-Login (authentication)
├── Flask-Session (server-side sessions)
├── Anthropic SDK (Claude API)
├── SQLite (development)
├── PostgreSQL (Render production)
└── Python 3.11+
```

---

## Architecture Inspiration

**From SHODANN (algorithm-shodann)**:
- 4-layer prompt structure (context, data, pedagogical, format)
- Pedagogical guardrails ("growth opportunity" not "error")
- Per-student state management (we use per-group)

**From PocketFlow Chatbot (tool-algoflow-py)**:
- Session management patterns
- API endpoint design
- Queue management concepts (though we don't need queuing)

**From AlgoCratic Capstone**:
- Per-group context injection
- Clearance-level awareness
- Sacred Workflow emphasis

---

## Core Files to Create

### 1. `app.py` - Main Application
```python
from flask import Flask, render_template, session, request, jsonify
from anthropic import Anthropic
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Routes:
# GET  /           → login page
# POST /login      → authenticate group
# GET  /chat       → chat interface
# POST /api/chat   → send message, get response
# GET  /admin      → instructor dashboard
# GET  /logout     → end session
```

### 2. `auth.py` - Authentication Logic
```python
# Group credentials (production: database)
GROUPS = {
    'group1': {'password': 'capstone2026', 'clearance': 'ORANGE'},
    'group2': {'password': 'dataman2026', 'clearance': 'YELLOW'},
    # ...
}

def authenticate_group(group_id, password):
    """Verify group credentials"""
    pass

def get_group_context(group_id):
    """Load group's project context"""
    pass
```

### 3. `claude_handler.py` - API Integration
```python
def build_system_prompt(group_context):
    """
    Build pedagogical system prompt with group context.
    
    Inspired by SHODANN's 4-layer prompt structure:
    1. Context Layer: Group project details
    2. Data Layer: (N/A for chat, used in PR feedback)
    3. Pedagogical Layer: Teaching rules
    4. Format Layer: Response style
    """
    return f\"\"\"You are an AI teaching assistant for AlgoCratic Futures capstone course.

CURRENT GROUP CONTEXT:
{group_context}

PEDAGOGICAL RULES:
1. Never provide direct solutions - guide through iteration
2. Require students to explain their attempt first
3. Ask clarifying questions before answering
4. Emphasize Sacred Workflow (Issue → Branch → PR → Review)
5. Reference their project context when relevant
6. Celebrate iteration and learning velocity

VOCABULARY:
- "Growth opportunity" NOT "error"
- "Suboptimal" NOT "wrong"
- "The Algorithm suggests" NOT "You should"

RESPONSE STYLE:
- Technical but encouraging
- Light AlgoCratic voice (5% seasoning)
- Competence over entertainment
\"\"\"

def get_claude_response(group_id, user_message, conversation_history):
    """Call Claude with context and conversation history"""
    pass
```

### 4. `models.py` - Database Models
```python
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    clearance_level = db.Column(db.String(20))
    token_budget = db.Column(db.Integer, default=100000)
    tokens_used = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    role = db.Column(db.String(20))  # 'user' or 'assistant'
    content = db.Column(db.Text)
    tokens_used = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### 5. UI Files

**`templates/login.html`** - Login page
**`templates/chat.html`** - Chat interface with terminal aesthetic
**`templates/admin.html`** - Instructor dashboard
**`static/css/terminal.css`** - AlgoCratic styling

See parallel plan for complete HTML/CSS.

---

## Context File Format

Each group gets a context file: `context/group_N_context.md`

```markdown
# Group N Context

## Project Overview
- Product: DataMan Math Platform
- Tech Stack: Flask, SQLite, React
- Current Sprint: Sprint 2 - User Authentication

## Team Members
- Student A (team lead)
- Student B (backend)
- Student C (frontend)

## Current Sprint Focus
Implementing user authentication and database integration.

## Known Issues
- Issue #12: Flask-SQLAlchemy migration failing
- Issue #15: Login route returning 500

## Recent Progress
- Completed wireframes for all pages
- Set up PostgreSQL on Render
- Implemented basic routing structure

## Clearance Level
ORANGE → YELLOW (transitioning)
```

---

## Deployment Configuration

**`requirements.txt`**:
```
flask==3.0.0
anthropic==0.18.0
flask-login==0.6.3
flask-sqlalchemy==3.1.1
python-dotenv==1.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

**`render.yaml`** - See parallel plan for complete config

**Environment Variables** (set in Render dashboard):
- `ANTHROPIC_API_KEY`
- `FLASK_SECRET_KEY`
- `ADMIN_PASSWORD`
- `DATABASE_URL` (auto-generated by Render)

---

## Development Workflow

### Phase 1: Core (Hours 0-4)
1. Create Flask skeleton with routes
2. Test Claude API integration (hardcoded context)
3. Build basic chat interface (terminal aesthetic)
4. Get one complete conversation working

**Exit Criteria**: Can send message, get Claude response, no persistence yet

### Phase 2: Persistence (Hours 4-8)
1. Set up SQLite database with models
2. Implement conversation logging
3. Add token usage tracking
4. Create admin view of conversations

**Exit Criteria**: Conversations persist, token usage tracked, visible in admin dashboard

### Phase 3: Context (Hours 8-12)
1. Create per-group context files
2. Load context in Claude handler
3. Test context-aware responses
4. Verify group isolation (groups can't see each other)

**Exit Criteria**: Claude responses reference group project, clearance level

### Phase 4: Deployment (Hours 12-16)
1. Switch to PostgreSQL for Render
2. Test database migrations
3. Configure Render deployment
4. Deploy and smoke test

**Exit Criteria**: Running on Render, accessible via URL

### Phase 5: Polish (Hours 16-20)
1. Error handling (API failures, rate limits)
2. Security review (XSS, SQL injection, session security)
3. Documentation (setup guide, admin guide)
4. Final testing with multiple groups

**Exit Criteria**: Production-ready, documented, tested

---

## Coordination with Instance B

### Shared Files You'll Touch

**`shared/database_schema.sql`**:
- You own: groups, conversations, messages tables
- Instance B may add: api_usage table (for System 2 logging)
- Protocol: Create PR when modifying, wait for B's approval

**`shared/group_context_template.md`**:
- You define the format
- Instance B uses the same format in their CLAUDE.md templates
- Protocol: Propose format, B reviews and adopts

### Communication
- **Branch naming**: `system1/your-feature-name`
- **PR labels**: `system1`, `coordination` (if affects Instance B)
- **Blockers**: Create GitHub issue with `blocker` label

---

## Testing Checklist

- [ ] Group 1 can log in
- [ ] Group 2 can log in (separate conversations)
- [ ] Claude responses include project context
- [ ] Token usage increments correctly
- [ ] Admin can view all conversations
- [ ] Admin can see token usage per group
- [ ] Groups can't access each other's conversations
- [ ] Handles Claude API errors gracefully
- [ ] Works on Render (PostgreSQL, not SQLite)
- [ ] Terminal aesthetic looks good

---

## Key Design Decisions

### Why Flask?
- Lightweight, suitable for MVP
- Easy to deploy on Render
- Good templating for terminal aesthetic
- Anthropic SDK works well with Flask

### Why SQLite → PostgreSQL?
- SQLite for local development (simple)
- PostgreSQL for Render (Render provides free PostgreSQL)
- Models work with both via SQLAlchemy

### Why Group-Based Auth?
- Simpler than individual student accounts
- Matches team structure in capstone
- Easy credential distribution

### Why Server-Side Sessions?
- Secure (session data not in client)
- Persistent across page reloads
- Compatible with Render

---

## Success Criteria

### Technical
- ✅ <3 second response time
- ✅ Token tracking accurate within 1%
- ✅ No conversation data leakage between groups
- ✅ 99% uptime during alpha period

### Pedagogical
- ✅ Claude responses reference group project
- ✅ Pedagogical guardrails visible (asks questions, doesn't solve directly)
- ✅ Students report feeling supported, not just given answers
- ✅ Iteration encouraged (visible in conversation logs)

---

## Reference Materials

**Read these from the cloned repos**:
- `/home/claude/algorithm-shodann/design_docs/SHODANN_VOICE_GUIDE.md` - Pedagogical tone
- `/home/claude/algorithm-shodann/prompts/01_base_shodann_prompt.md` - Prompt structure
- `/home/claude/tool-algoflow-py/docs/planning/chatbot-mvp-prd.md` - Session management patterns

**Read this for overall plan**:
- `/home/claude/TA_SYSTEMS_PARALLEL_PLAN.md` - Complete parallel development plan

---

## When You're Ready

1. Create `app.py` with basic Flask skeleton
2. Test Claude API connection
3. Build chat UI
4. Add database models
5. Implement logging
6. Deploy to Render

**Your first task**: Create `app.py` with a working Flask app that can send a message to Claude and get a response. Everything else builds on this foundation.

frotz → The Algorithm awaits your implementation.
