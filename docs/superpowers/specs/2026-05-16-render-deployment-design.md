---
title: Render Deployment — System 1 (teacherbot), CLI-driven
date: 2026-05-16
status: approved
supersedes: docs/superpowers/specs/2026-05-13-render-deployment-design.md
---

# Render Deployment Design — Revision 2 (CLI-driven)

## Why this exists

The 2026-05-13 design assumed a set of `mcp__render__*` tools were available in
the agent session. That assumption was wrong in the working environment, so the
prior plan could not be executed verbatim. This revision targets the **Render
CLI** as the primary control plane, with the Render REST API as a documented
fallback. The 2026-05-13 spec and plan stay in the repo as historical record,
marked `SUPERSEDED`.

## Goal

Deploy `system1-flask-chat/` to Render as a Python web service backed by a
managed PostgreSQL database. The old misconfigured `tool-teacherbot` service is
deleted *before* the new one is created so the workspace ends in a clean,
single-service state. After this work lands, pushing to `main` triggers an
auto-deploy.

## Current state (2026-05-16)

- Render workspace contains one stale service: `tool-teacherbot`
  (srv-d81rsrv7f7vs73eeihmg) — wrong `rootDir`, wrong `startCommand`, no DB,
  no env vars. It must be removed.
- No managed Postgres instances exist in the workspace.
- The repo's `main` branch already contains:
  - the Flask app (`system1-flask-chat/`)
  - `render.yaml` (Blueprint config — see audit below)
  - `runtime.txt` pinned to `python-3.11.9`
  - `requirements.txt` with `psycopg[binary]>=3.1` and `gunicorn==21.2.0`
  - `app.py` already normalizes `postgres://` and `postgresql://` URLs to the
    `postgresql+psycopg://` dialect (SQLAlchemy + psycopg3)
- PR #1 is open but stale: every commit on its branch is already present on
  `main`, plus 14 more.
- Render MCP tools are **not** available in the agent session. Render CLI is
  also not installed locally.

## Resources to create / destroy

### Destroy

| Resource | ID | Reason |
|---|---|---|
| Web service `tool-teacherbot` | srv-d81rsrv7f7vs73eeihmg | Misconfigured, no DB, never reached live state. |

### Create

**PostgreSQL database**

| Property | Value |
|---|---|
| Name | `teacherbot-db` |
| Plan | `free` |
| Region | `virginia` |
| Version | 16 |
| Database name | Render-assigned (CLI does not accept a custom value) |
| User | Render-assigned |

**Web service**

| Property | Value |
|---|---|
| Name | `teacherbot` |
| Repo | https://github.com/norrisaftcc/tool-teacherbot |
| Branch | `main` |
| Root directory | `system1-flask-chat` |
| Runtime | Python |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn "app:create_app()"` |
| Region | `virginia` |
| Plan | `free` |
| Auto-deploy | on push to `main` |

> **Public URL:** the service URL is assigned by Render at creation. It will
> resemble `https://teacherbot.onrender.com` but may receive a random suffix
> if the name is taken at the platform level. The actual URL is recorded in the
> tracking issue after the service is created.

## Environment variables

All four are set at service creation time (not edited in afterwards):

| Variable | Source | Notes |
|---|---|---|
| `ANTHROPIC_API_KEY` | provided by instructor | `sk-ant-…`; never logged |
| `FLASK_SECRET_KEY` | `python3 -c "import secrets; print(secrets.token_hex(32))"` | 64-char hex; rotate on suspected leak |
| `ADMIN_PASSWORD` | chosen by instructor | gates `/admin?password=…` query string; alpha-grade |
| `DATABASE_URL` | connection string from `teacherbot-db` | starts with `postgresql://`; `app.py:18-21` rewrites scheme |

The Render-generated `DATABASE_URL` includes the hostname, port, generated
user/password, and generated database name. Using it verbatim is required
because the CLI does not accept custom database/user names at creation time.

## Tooling split — who does what

| Step | Actor | How |
|---|---|---|
| Install Render CLI | user | `brew install render` |
| Authenticate Render CLI | user | `render login` (browser-based OAuth) |
| Generate `FLASK_SECRET_KEY` | user | one-line python invocation, captured into shell variable |
| Provide `ANTHROPIC_API_KEY` | user | pasted into prompt when the agent needs it |
| Delete old `tool-teacherbot` service | agent | `render services delete <id>` after confirming ID via `render services` |
| Create Postgres DB | agent | `render postgres create` |
| Create web service with all env vars inline | agent | `render services create` |
| Tail initial deploy logs | agent | `render logs --resources <service-id> --tail` |
| HTTP smoke test (`/`, `/login`, `/admin`) | agent | `curl` against the live URL |
| Browser smoke test (chat streaming) | user | manual; agent watches logs in parallel |

### Fallback if CLI subcommands are unavailable

The Render CLI is in active development; subcommand names occasionally change
between releases. If a needed subcommand is missing, the agent falls back to
the REST API at `https://api.render.com/v1/` using the `RENDER_API_KEY`
generated from the Render dashboard. The fallback is documented in
`system1-flask-chat/DEPLOY.md` so a human operator can repeat it.

## Repo changes (the deploy PR)

Branch: `system1/deploy-render`. Files added or modified:

| Path | Change | Rationale |
|---|---|---|
| `docs/superpowers/specs/2026-05-16-render-deployment-design.md` | **new** | This document. |
| `docs/superpowers/plans/2026-05-16-render-deployment.md` | **new** | Step-by-step implementation plan written by the writing-plans skill. |
| `docs/superpowers/specs/2026-05-13-render-deployment-design.md` | banner | Prepend `> **SUPERSEDED by 2026-05-16-render-deployment-design.md.**` |
| `docs/superpowers/plans/2026-05-13-render-deployment.md` | banner | Same. |
| `system1-flask-chat/DEPLOY.md` | **new** | Operator runbook: required env vars, redeploy steps, log access, rollback, CLI vs REST fallback. |
| `render.yaml` | edit | Rename service `algocratic-ta-system1` → `teacherbot`; rename database `algocratic-ta-db` → `teacherbot-db`; drop custom `databaseName: ta_system` and `user: ta_admin` (CLI-created DB will use Render-assigned values, and keeping the YAML divergent would make a future Blueprint re-creation produce a different DB than the running one). |
| `README.md` | small edit | Add one-line pointer to `system1-flask-chat/DEPLOY.md`. |

No app code changes are made in this PR. Any issues surfaced during the audit
become separate follow-up issues, not in-scope edits.

## Verification

After the service reports `live`:

1. `curl -sI https://<service-url>/` → 200 or 302.
2. `curl -i -X POST -d 'group_id=group1&password=capstone2026' https://<service-url>/login` →
   302 with `Location: /chat`.
3. Browser walk-through (user): log in as `group1` / `capstone2026`, send a
   chat message, confirm streaming token-by-token render.
4. `curl -sI 'https://<service-url>/admin?password=<ADMIN_PASSWORD>'` → 200.
5. Push a trivial doc-only commit to `main`; confirm a new deploy starts
   automatically and reaches `live`.

## Rollback

- **First deploy fails build/boot:** read `render logs`, fix the root cause in
  a follow-up commit on `main`. Do not work around hooks. Do not amend.
- **Later deploy breaks prod:** `render deploys list` → `render deploys rollback
  <prev-deploy-id>`. DB schema is `db.create_all()` only with no destructive
  migrations, so reverting code is safe.
- **Worst case:** suspend the service (free tier supports this) without
  destroying the DB; investigate offline; redeploy when fixed.

## Out of scope

- Filling in `system1-flask-chat/context/group*_context.md` placeholder
  templates with real project briefs (instructor task, tracked separately).
- System 2 (`system2-code-distribution/`) — separate deployment.
- Custom domain or TLS configuration.
- Scaling beyond Render free tier (web service spins down after 15 min idle).
- Replacing query-string admin auth with a proper login form (known alpha-grade
  weakness; flagged in `current-status-report.md`).
- Adding CSRF tokens (known weakness; same source).

## Success criteria

- `https://<service-url>/` returns the login page.
- `group1` / `capstone2026` login succeeds and `/chat` renders the UI.
- A chat message produces a streamed response from Claude.
- `/admin?password=<ADMIN_PASSWORD>` lists the conversation just created.
- Pushing a no-op commit to `main` triggers an auto-deploy that reaches `live`
  within 5 minutes.
- The old `tool-teacherbot` service is gone from the workspace.
- A GitHub issue exists with a comment trail of every CLI command run, so the
  next operator can repeat or audit the deploy without reading agent
  transcripts.
