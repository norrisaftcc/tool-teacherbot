# System 1 — Teacherbot Flask Chat (Demo)

Group-authenticated chat that injects per-group capstone context into Claude.
This README covers running it locally in a Codespace for a short demo.
Render deployment will be a follow-up PR.

## Quick Start (Codespace / local)

```bash
cd system1-flask-chat
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env: set ANTHROPIC_API_KEY at minimum.

python app.py
```

App runs on `http://localhost:5000` (binds 0.0.0.0 so it works from a Codespace
forwarded port).

## Demo Credentials

| Group  | Password         | Clearance |
|--------|------------------|-----------|
| group1 | capstone2026     | ORANGE    |
| group2 | dataman2026      | YELLOW    |
| group3 | finaid2026       | ORANGE    |
| group4 | health2026       | YELLOW    |
| group5 | sched2026        | ORANGE    |

Defined in `auth.py`. Each group has a context file in `context/` injected
into Claude's system prompt on every chat call.

## Admin Console

Navigate to `/admin`. Default admin password is `admin` (override with
`ADMIN_PASSWORD` env var). Shows per-group token usage and recent
conversation logs.

## Tests

```bash
pytest tests/ -v
```

## Environment Variables

| Var                  | Default            | Notes                                  |
|----------------------|--------------------|----------------------------------------|
| `ANTHROPIC_API_KEY`  | _required_         | Claude API key                         |
| `FLASK_SECRET_KEY`   | `dev-secret-...`   | Override for any non-toy deployment    |
| `ADMIN_PASSWORD`     | `admin`            | Admin console gate                     |
| `DATABASE_URL`       | `sqlite:///ta_system.db` | Swap to Postgres for Render later |
| `CLAUDE_MODEL`       | `claude-sonnet-4-5-20250929` | Override if needed           |
| `PORT`               | `5000`             | Flask listen port                      |

## File Layout

```
system1-flask-chat/
  app.py                 # Flask app factory
  routes.py              # Login / chat / api / admin routes
  auth.py                # Group credentials + context loader
  claude_handler.py      # Anthropic SDK + pedagogical system prompt
  models.py              # Group / Conversation / Message (SQLAlchemy)
  context/               # Per-group context markdown
  templates/             # Jinja templates
  static/css/            # Design tokens + kit + app gap-fillers
  static/js/chat.js      # Chat fetch loop
  static/img/            # Brand mark
  tests/                 # Pytest suite
```

## What's Stubbed / Out of Scope

- Render `render.yaml` and PostgreSQL switch — separate PR.
- Real user accounts (current alpha uses one shared password per group).
- Streaming responses (current API blocks until complete).
- Doc-panel artifact viewer from the design mockup.
