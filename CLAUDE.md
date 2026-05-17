# AlgoCratic TA Systems

Dual-system AI-assisted capstone education platform. System 1 (Flask chat) is **deployed and live**. System 2 (CLI distribution) is not yet started.

## Current state

| System | Status | Notes |
|---|---|---|
| **System 1** (`system1-flask-chat/`) | ✅ Live on Render | https://teacherbot-6yut.onrender.com/ |
| **System 2** (`system2-code-distribution/`) | ⛔ Not started | Directory does not exist yet |
| `shared/` | ⛔ Not created | No cross-system code exists yet |

## What's where

| Path | Purpose |
|---|---|
| `system1-flask-chat/` | Flask app: group login → Claude API with per-group context injection → conversation log |
| `system1-flask-chat/DEPLOY.md` | **Operator runbook** — env vars, redeploy, logs, rollback, suspend |
| `system1-flask-chat/auth.py` | Hardcoded group credentials (group1–group5) — alpha-grade |
| `system1-flask-chat/context/group*_context.md` | Per-group project briefs injected into Claude prompts (placeholders — instructor fills in) |
| `docs/superpowers/specs/2026-05-16-render-deployment-design.md` | Current deploy spec |
| `docs/superpowers/plans/2026-05-16-render-deployment.md` | Step-by-step deploy procedure (idempotent) |
| `render.yaml` | Blueprint, kept in sync with what was deployed |
| `runtime.txt` | **NOT read by Render** — see Gotchas below |
| `SYSTEM1_CLAUDE.md` / `SYSTEM2_CLAUDE.md` | Historical: launch guides for the original two-instance development plan |
| `TA_SYSTEMS_PARALLEL_PLAN.md` | Historical: original 25KB technical spec |
| `docs/superpowers/specs/2026-05-13-*` and `plans/2026-05-13-*` | **SUPERSEDED** — kept for paper trail |

## How to work with the live service

- **Push to `main` triggers auto-deploy** (verified, ~1 min to live)
- Service ID: `srv-d84ha1og4nts73f73rng` · DB ID: `dpg-d84h9epkh4rs73d70pgg-a` · region `virginia` · free plan
- For deploys, env vars, logs, rollback: read `system1-flask-chat/DEPLOY.md` first
- Render CLI workspace: `render workspace set tea-d81rjp0sfn5c738tl430` (one-time per shell)

## Architecture

```
System 1 (deployed):
  Flask + gunicorn  ──►  Anthropic API
       │
       └──►  Render Postgres (teacherbot-db)
              ├── Group, Conversation, Message tables
              └── db.create_all() on startup (no migrations framework)

System 2 (not built):
  setup.py → per-group folders (API key + spend_cap.json + CLAUDE.md)
```

## Gotchas

### Repo-level

- **`runtime.txt` at the repo root is invisible to Render** because `rootDir: system1-flask-chat`. The Python version is pinned via `system1-flask-chat/.python-version`. Don't add a redundant `runtime.txt` inside the subdir — pick one mechanism.
- **The `system2-code-distribution/` and `shared/` directories don't exist yet.** Don't reference them as if they do.
- **`SYSTEM1_CLAUDE.md` and `SYSTEM2_CLAUDE.md` are not root CLAUDE.md files** — they were intended to be copied into subdirs at instance-launch time. System 1's CLAUDE.md derivation already happened; treat `SYSTEM1_CLAUDE.md` as historical.

### Render-level (live with these)

- **Same-region Postgres uses the internal connection string**, not the external one. External requires TLS handshake that flakes from within Render's network. Get the right one from `GET /v1/postgres/<id>/connection-info → internalConnectionString`.
- **Render CLI v2.17.0 cannot create Postgres or delete services.** Both gaps require the REST API (`POST /v1/postgres`, `DELETE /v1/services/<id>`). The CLI is fine for service create/update/restart/deploys/logs.
- **Render CLI `--output json` writes ANSI escape codes when stdout isn't a TTY**, breaking jq. Use REST API directly when scripting.
- **Free-tier Postgres has a 30-day rolling expiry** and the workspace allows one free Postgres at a time. Don't try to create a second one without deleting the first.
- **Blueprint apply via dashboard requires payment info on file** (workspace eligibility), even for free-tier resources. The CLI+REST path doesn't.

### App-level (known alpha-grade issues)

- Admin auth is `?password=...` query string. Replace with a POST form before classroom use.
- No CSRF protection. `flask-wtf` is not in requirements.
- Token-budget enforcement has a race condition (read-modify-write between requests is not atomic).
- `db.create_all()` runs on every startup; there's no migrations framework.

## Tech stack

- **System 1**: Flask 3.x, Flask-SQLAlchemy, Anthropic SDK 0.101.0, psycopg3, gunicorn, Python 3.11.9 on Render free tier
- **System 2** (planned): Python 3.11+, argparse, pathlib (no external deps by design)

## Branch / PR conventions

- Branch names: `system1/feature-name` and (future) `system2/feature-name`
- Open a PR for non-trivial changes, even when working solo — keeps a reviewable record
- Direct commits to `main` are acceptable for one-line deploy-blocker fixes (Python pinning, env var corrections); document the why in the commit message and reference the relevant issue
