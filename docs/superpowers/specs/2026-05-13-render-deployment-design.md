> **SUPERSEDED — do not act on this document.**
>
> A May 2026 plan for a stack that no longer exists. It provisions free-tier
> Render resources under names (`teacherbot-db`) that were replaced by the Pro
> Blueprint in `render.yaml`, and the database it describes has since been
> deleted. It also predates Alembic (ADR-0006), so any schema reasoning in it is
> wrong.
>
> It is kept for the reasoning, not the steps. Current operator truth is
> `system1-flask-chat/DEPLOY.md`; current decisions are `docs/registry/KEEP.md`.
>
> This banner exists because the file opens by instructing an agent to execute
> it task-by-task, which is the one kind of stale document that can do damage.

---
title: Render Deployment — System 1 (algocratic-ta-system1)
date: 2026-05-13
status: superseded
---

> **SUPERSEDED by `docs/superpowers/specs/2026-05-16-render-deployment-design.md`.**
> This document assumed Render MCP tools that were not available in the agent
> environment. The 2026-05-16 revision drives the deploy via Render CLI plus
> targeted REST calls and renames the service to `teacherbot`.

# Render Deployment Design

## Goal

Deploy System 1 (Flask chat TA interface) to Render with a PostgreSQL database, replacing
the existing misconfigured `tool-teacherbot` service.

## Current State

- Render workspace: `My Workspace` (tea-d81rjp0sfn5c738tl430)
- Existing service: `tool-teacherbot` (srv-d81rsrv7f7vs73eeihmg) — misconfigured
  - rootDir is empty (should be `system1-flask-chat`)
  - startCommand is `gunicorn your_application.wsgi` (wrong)
  - No PostgreSQL database attached
  - No env vars set
- No PostgreSQL instances exist in the workspace

## Resources to Create

### 1. Delete old service
- Service: `tool-teacherbot` (srv-d81rsrv7f7vs73eeihmg)
- Reason: wrong rootDir, wrong startCommand, wrong name

### 2. PostgreSQL database
- Name: `algocratic-ta-db`
- DB name: `ta_system`
- User: `ta_admin`
- Region: Virginia (us-east)
- Plan: free

### 3. Web service
- Name: `algocratic-ta-system1`
- Repo: `https://github.com/norrisaftcc/tool-teacherbot`
- Branch: `main`
- rootDir: `system1-flask-chat`
- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn "app:create_app()"`
- Region: Virginia (us-east)
- Plan: free
- Auto-deploy: on commit to main

## Environment Variables

| Variable | Source |
|---|---|
| `ANTHROPIC_API_KEY` | Provided by instructor at deploy time |
| `FLASK_SECRET_KEY` | Generated random string |
| `ADMIN_PASSWORD` | Set by instructor at deploy time |
| `DATABASE_URL` | Linked from `algocratic-ta-db` connection string; `app.py` already handles `postgres://` → `postgresql://` rewrite |

## Application Notes

- Auth is hardcoded in `auth.py` for groups 1–5 with passwords defined there
- Context files (`system1-flask-chat/context/group*_context.md`) are placeholder templates — instructors must fill these in before students use the app
- `db.create_all()` runs on startup; no separate migration step needed
- Streaming SSE responses require `X-Accel-Buffering: no` header (already set in routes.py)

## Out of Scope

- Filling in group context files (separate instructor task)
- System 2 (CLI distribution framework) — separate deployment
- Custom domain setup
- Scaling beyond free tier

## Success Criteria

- `https://algocratic-ta-system1.onrender.com/` shows login page
- Login as `group1` / `capstone2026` succeeds
- Chat sends a message and receives a streamed Claude response
- Admin dashboard accessible at `/admin?password=<ADMIN_PASSWORD>`
- Conversations logged to PostgreSQL
