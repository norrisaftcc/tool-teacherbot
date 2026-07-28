# System 1 — Render Deployment Runbook

This document describes how `teacherbot` is deployed on Render and how to
operate it. The deploy was originally provisioned by a one-time bootstrap
procedure documented in `docs/superpowers/plans/2026-05-16-render-deployment.md`.

## Service summary

| Property | Value |
|---|---|
| Service name | `teacherbot` |
| Database name | `teacherbot-db` |
| Region | Virginia (us-east) |
| Plan | free (web + DB) |
| Branch deployed | `main` |
| Root directory | `system1-flask-chat` |
| Auto-deploy | enabled (every push to `main`) |
| Service URL | recorded in tracking issue at first deploy |

## Required environment variables

| Variable | Source / how to set |
|---|---|
| `ANTHROPIC_API_KEY` | Instructor's key from https://console.anthropic.com/. Starts with `sk-ant-`. |
| `FLASK_SECRET_KEY` | Generated random hex: `python3 -c "import secrets; print(secrets.token_hex(32))"`. Rotate on suspected leak. |
| `ADMIN_PASSWORD` | Chosen string. Gates `/<slug>/admin?password=…` per skin (e.g. `/csc114/admin?password=…`). Alpha-grade auth — replace before public use. |
| `DATABASE_URL` | Connection string from the `teacherbot-db` instance. `app.py:18-21` rewrites `postgres://` and `postgresql://` to `postgresql+psycopg://`. |

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
# Suspend (free tier; DB is preserved):
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

These are documented in `../current-status-report.md` and are out of scope for
the initial deploy. File issues to track them before any production use:

- Admin auth is `/<slug>/admin?password=...` query string. Replace with a POST login form.
- No CSRF protection. `flask-wtf` is not in `requirements.txt`.
- Token-budget enforcement has a race condition (read-modify-write between
  requests is not atomic).
- `db.create_all()` runs on every startup; there is no migrations framework.

## Re-creating the service from scratch

If `teacherbot` ever needs to be recreated, the canonical procedure is in
`../docs/superpowers/plans/2026-05-16-render-deployment.md`. The `render.yaml`
Blueprint at the repo root is kept in sync with the deployed state and is also
a valid (though manual) starting point if you prefer the "New Blueprint" flow
in the Render dashboard — note that the dashboard requires a payment method
on file before it will apply a Blueprint, even for free-tier resources.

<!-- deploy verified 2026-05-17T01:46:44Z -->
