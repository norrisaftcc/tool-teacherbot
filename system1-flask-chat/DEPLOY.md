# System 1 — Render Deployment Runbook

This document describes how `teacherbot` is deployed on Render and how to
operate it. The deploy was originally provisioned by a one-time bootstrap
procedure documented in `docs/superpowers/plans/2026-05-16-render-deployment.md`.

## Service summary

| Property | Value |
|---|---|
| Service name | `teacherbot` |
| Database name | `teacherbot-db` (+ `teacherbot-db-staging` for migration rehearsal) |
| Region | Virginia (us-east) |
| Plan | Pro (web + DB) |
| Branch deployed | `main` |
| Root directory | `system1-flask-chat` |
| Auto-deploy | enabled (every push to `main`) |
| Pre-deploy | `flask db upgrade` — migrations run before traffic shifts |
| Service URL | recorded in tracking issue at first deploy |

> **Rebuilt on Pro tier, 2026-07-29.** The original free-tier stack
> (`srv-d84ha1og4nts73f73rng`) was written off rather than migrated. Free
> Postgres carries a 30-day rolling expiry and that instance was ~73 days old,
> so it had most likely already lapsed. Starting from an empty database is also
> what let Alembic adopt the schema without a hand-run `flask db stamp head`
> against production — see ADR-0006.

## Required environment variables

| Variable | Source / how to set |
|---|---|
| `ANTHROPIC_API_KEY` | Instructor's key from https://console.anthropic.com/. Starts with `sk-ant-`. |
| `FLASK_SECRET_KEY` | Generated random hex: `python3 -c "import secrets; print(secrets.token_hex(32))"`. Rotate on suspected leak. |
| `ADMIN_PASSWORD` | Chosen string. Gates `/<slug>/admin?password=…` per skin (e.g. `/csc114/admin?password=…`). Alpha-grade auth — replace before public use. |
| `DATABASE_URL` | Connection string from the `teacherbot-db` instance. Use the **internal** one — the external requires a TLS handshake that flakes from inside Render's network. `app.py` rewrites `postgres://` and `postgresql://` to `postgresql+psycopg://`. |
| `FLASK_APP` | `app:create_app`. Required by `flask db upgrade` in the pre-deploy command; without it the deploy fails before the app starts. |

**`FLASK_SECRET_KEY` and `ADMIN_PASSWORD` are now hard requirements.** They
used to fall back to `dev-secret` and `admin`, so a service missing either
came up looking healthy while signing session cookies with a value published
in this public repo — anyone could forge `session['skin']` and skip the
cohort passcode. `create_app` now raises at startup instead. If a deploy
fails with *"Refusing to start: … not set"*, that is this check; set the
variable and redeploy.

## Optional environment variables

| Variable | Effect |
|---|---|
| `<SLUG>_ACTIVE_MODULE` | Advance the corpus window without a commit, e.g. `CSC134_ACTIVE_MODULE=m3`. A value that resolves to no corpus path is logged and ignored rather than blanking the prompt. |
| `CSC134_PASSCODE` | Override the cohort passcode in `auth.py`. Set this to rotate without publishing the new value in a public commit. |
| `GROUP_TOKEN_BUDGET` | Per-cohort token ceiling for newly created groups (default 25,000,000). Existing rows are lifted to the default at next login — a column default only applies on INSERT, and there is no migrations framework. |

Read or update env vars:

```bash
# Read (requires RENDER_API_KEY)
curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
  https://api.render.com/v1/services/<srv-id>/env-vars | jq .

# Update one (without restarting):
curl -s -X PUT \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '[{"key":"ADMIN_PASSWORD","value":"new-value"}]' \
  https://api.render.com/v1/services/<srv-id>/env-vars
```

## Schema changes

The production schema is owned by Alembic (ADR-0006). `db.create_all()` still
exists but runs only under `TESTING` — the two must never both touch a real
database, because `create_all` writes no `alembic_version` row and the next
migration then fails on a table that already exists.

### Making one

```bash
cd system1-flask-chat
# after editing models.py
flask db migrate -m "what changed and why"
# read the generated file before committing it — autogenerate misses
# server defaults, renames (it sees drop+add), and CHECK constraints
flask db upgrade && flask db downgrade && flask db upgrade   # round-trip
flask db check                                               # no drift
```

CI runs `tests/test_migrations.py`, which applies the migrations to a real
database and diffs the result against `db.metadata`. A model changed without a
migration is a red build, not a production incident.

### Rehearsing on staging — do this before merging

The test suite runs on SQLite, which accepts things Postgres rejects: type
changes, constraints added against existing data, a non-null column on a
populated table. A green suite is not evidence that a migration survives real
data.

```bash
# Internal connection string for teacherbot-db-staging
export DATABASE_URL='<staging-internal-url>'
export FLASK_APP=app:create_app
cd system1-flask-chat && flask db upgrade

python3 -c "
from sqlalchemy import create_engine, inspect
import os
print(sorted(inspect(create_engine(os.environ['DATABASE_URL'].replace(
    'postgres://', 'postgresql+psycopg://', 1))).get_table_names()))"
# expect: alembic_version, conversations, groups, messages
```

Only then merge to `main`. Auto-deploy runs `flask db upgrade` as its pre-deploy
step; if the migration fails, the deploy is blocked and the running version keeps
serving.

### If a migration fails in pre-deploy

The deploy stops and the previous version stays live — that is the intended
behaviour, so there is no outage to race. Fix forward: correct the migration,
push, let the next deploy run it. Do not roll the *service* back to escape a bad
migration; the schema is what needs reverting, and `flask db downgrade` against
the database is the tool for that.

## Common operations

### Find the service ID

```bash
render workspace set tea-d81rjp0sfn5c738tl430   # one-time per shell
render services --output json | jq -r '.[] | select(.service.name=="teacherbot") | .service.id'
```

### Trigger a manual deploy

Auto-deploy fires on every push to `main`. To force one without a push:

```bash
render deploys create <srv-id>
```

### Tail logs

```bash
render logs --resources <srv-id>
```

### Roll back to a previous deploy

```bash
render deploys list <srv-id> --output json | jq -r '.[] | "\(.deploy.id)  \(.deploy.status)  \(.deploy.commit.id[:7])"'
# Pick a deploy ID with status=live from before the bad change:
render deploys rollback <srv-id> --deploy-id <dep-...>
```

> As of Render CLI v2.17.0, `deploys rollback` may not be available; if so,
> use the dashboard's "Deploys" tab on the service: click the previous
> successful deploy and press "Rollback".

### Suspend / resume the service

```bash
# Suspend (the database is preserved; on Pro it keeps billing):
curl -s -X POST -H "Authorization: Bearer $RENDER_API_KEY" \
  https://api.render.com/v1/services/<srv-id>/suspend

# Resume:
curl -s -X POST -H "Authorization: Bearer $RENDER_API_KEY" \
  https://api.render.com/v1/services/<srv-id>/resume
```

### Restart the service (without redeploy)

```bash
render restart <srv-id>
```

## Known alpha-grade issues

All tracked as issues and indexed in `../docs/registry/KEEP.md`. This list used
to say "file issues to track them before any production use" and nobody did for
two months, which is why the register exists.

- Admin auth is `/<slug>/admin?password=...` query string — #26.
- No CSRF protection; `flask-wtf` is not in `requirements.txt` — #27.
- `increment_tokens` has a read-modify-write race — #28.
- `marked` is loaded from a CDN unpinned and unhashed — #25.
- Corpus manifests track a moving branch — #24.

Resolved since: `db.create_all()` no longer runs in production (ADR-0006), and
the secrets no longer have fallbacks.

## Re-creating the stack from scratch

**The Blueprint is now the canonical path.** Applying it from the dashboard
requires a payment method on file, which is why the original bootstrap went
through CLI + REST instead; Pro tier satisfies that, so "New Blueprint" against
`render.yaml` reproduces the web service, the database, and staging in one go.

Before applying, replace the three `plan:` placeholders in `render.yaml` with
real paid plan identifiers. They are deliberately invalid so an unedited apply
fails loudly — leaving the database as `free` would silently re-inherit the
30-day expiry this rebuild exists to escape.

Then, once:

```bash
# Set the three sync:false secrets in the dashboard, then confirm the schema
# built. On a fresh database this is the first `flask db upgrade`; no
# `stamp head` is needed, which is the point of rebuilding rather than migrating.
render logs --resources <srv-id> | grep -i alembic
curl -sS -o /dev/null -w '%{http_code}\n' https://<service>.onrender.com/
```

The CLI + REST procedure in
`../docs/superpowers/plans/2026-05-16-render-deployment.md` still works and is
the fallback if the Blueprint flow is unavailable.

The real smoke test after any deploy is a `/csc134/` login: `do_login` queries
the database without exception handling, so it is the path that fails loudly if
the schema or connection string is wrong. `/` renders without touching the
database and will happily return 200 over a broken one.

<!-- deploy verified 2026-05-17T01:46:44Z -->
