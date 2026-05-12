# System 1 Design: Flask Chat Interface

**Date:** 2026-05-12
**Status:** Approved
**Scope:** MVP alpha — local development first, Render deploy after stable

---

## Goals

Provide capstone students with a group-authenticated, context-aware Claude chat interface. Instructors can monitor conversations and token usage via a basic admin view.

**MVP requirements:**
- Group login (5 groups, hardcoded credentials)
- Chat with Claude (context-aware, pedagogical guardrails)
- Conversation logging to database
- Basic admin view (all groups, recent messages, token usage)

**Explicitly out of scope for MVP:**
- Individual student accounts
- Real-time token spend display in chat
- Growth velocity / GitHub commit tracking
- Multiple clearance levels
- PostgreSQL (SQLite locally until Render deploy)

---

## Architecture

Structured Flask app with strict layer separation:

| Layer | Files | Responsibility |
|-------|-------|---------------|
| UI | `templates/`, `static/` | Rendering only — no logic beyond Jinja2 conditionals |
| Routes | `app.py` | Route registration, request/response, delegates to business logic |
| Business logic | `auth.py`, `claude_handler.py` | Validation, API calls, prompt construction |
| Data | `models.py` | SQLAlchemy models, DB queries — no Flask imports beyond SQLAlchemy |

---

## File Structure

```
system1-flask-chat/
├── app.py                    # App factory, route registration, config
├── auth.py                   # Group credential validation, login/logout logic
├── claude_handler.py         # Claude API calls, system prompt construction
├── models.py                 # SQLAlchemy models: Group, Conversation, Message
├── requirements.txt
├── .env.example
├── templates/
│   ├── login.html
│   ├── chat.html
│   └── admin.html
└── static/
    ├── css/
    │   └── terminal.css      # Driven by docs/design/design-guidelines.md
    └── js/
        └── chat.js           # Async message send/receive (no full page reload)
context/
    ├── group_1_context.md
    ├── group_2_context.md
    └── ...                   # One file per group, loaded at login
```

---

## Data Models

```python
# models.py

class Group:
    id              Integer, PK
    name            String(50), unique      # "group1" .. "group5"
    clearance_level String(20)              # "ORANGE", "YELLOW", etc.
    token_budget    Integer, default=100000
    tokens_used     Integer, default=0
    created_at      DateTime

class Conversation:
    id          Integer, PK
    group_id    FK → Group
    started_at  DateTime

class Message:
    id              Integer, PK
    conversation_id FK → Conversation
    role            String(20)    # "user" | "assistant"
    content         Text
    tokens_used     Integer
    created_at      DateTime
```

**Auth:** Group credentials are a hardcoded dict in `auth.py` for the alpha. No `User` DB model.
**Context:** Loaded from `context/group_N_context.md` at login, stored in Flask session. No DB column, no per-message disk read.

---

## Routes

| Method | Route | Notes |
|--------|-------|-------|
| GET | `/` | Redirect to `/chat` if logged in, else login page |
| POST | `/login` | Validate creds, load context into session, redirect to `/chat` |
| GET | `/chat` | Login-required, render chat UI |
| POST | `/api/chat` | Login-required, returns JSON `{response, tokens_remaining}` |
| GET | `/admin` | Password-protected, shows all groups + conversation logs |
| GET | `/logout` | Clear session, redirect to `/` |

---

## Chat Data Flow

```
Student types message
  → POST /api/chat
    → Flask-Login auth check
    → claude_handler.build_system_prompt(session['group_context'])
    → claude_handler.get_response(conversation_history, user_message)
      → Anthropic SDK call
      → returns content + token count
    → Message.save(user_msg) + Message.save(assistant_msg)
    → Group.increment_tokens(tokens_used)
    → return JSON {response, tokens_remaining}
  → chat.js appends message to conversation UI (no page reload)
```

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Claude API timeout / failure | Return JSON error, display inline in chat UI, log failure — do not crash page |
| Token budget exhausted | Block `/api/chat`, show "budget reached" message in UI, group still visible in admin |
| Group context file missing | Fail at login with clear message — do not allow entry to chat without context |
| DB write failure | Log and continue — don't block student's chat response over a logging failure |

---

## Design

UI driven by `docs/design/design-guidelines.md` (maintained by design specialist).
AlgoCratic aesthetic: terminal-style, dark background, monospace font, green primary text.
`terminal.css` and templates are implemented from that spec — no design decisions in code.

---

## Deployment Path

1. Local: SQLite, `.env` file, `flask run`
2. Render: PostgreSQL (SQLAlchemy connection string swap), environment vars in Render dashboard, `gunicorn` via `render.yaml`

SQLAlchemy abstracts the difference — no model changes required for the switch.
