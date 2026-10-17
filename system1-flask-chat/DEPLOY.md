# System 1 — Render Deployment Runbook

This document describes how `teacherbot` is deployed on Render and how to
operate it. The deploy was originally provisioned by a one-time bootstrap
procedure documented in
`../docs/historical/plans/2026-05-16-render-deployment.md`.

## Service summary

> **This table describes what `render.yaml` asks for, not a service anyone has
> confirmed exists.** The Blueprint has never been applied — its three `plan:`
> values are still the deliberately-invalid placeholders — and the free-tier stack
> it replaces is gone. **Nothing here is evidence that production is up.**
>
> The **Source** column says where each row comes from, and there are exactly
> three kinds:
>
> - **intended** — declared in `render.yaml`, never confirmed against a live service.
> - **repo fact** — checkable from this repo today, including the absences.
> - **in the code** — implemented in the app itself.
>
> Once the real state is established from the Render dashboard, replace the
> **intended** rows with what actually exists and say so in the Source column.
> A row that stays **intended** is a row nobody has verified.

| Property | Value | Source |
|---|---|---|
| Service name | `teacherbot-pro` | `render.yaml:27` — **intended** |
| Database name | `teacherbot-pro-db` (+ `teacherbot-pro-db-staging` for migration rehearsal) | `render.yaml:74,94` — **intended** |
| Region | **undeclared.** `render.yaml` has no `region:` key on the service or either database, so an apply takes Render's default rather than a pinned region. This previously read "Virginia (us-east)", which nothing in the repo supported. See the warning below — it is not only a documentation gap. | repo fact |
| Plan | **unset** — `render.yaml:33,79,95` still hold `REPLACE_WITH_PAID_*_PLAN`. The *account* is Pro tier, which is a different thing and is what satisfies the Blueprint's payment-method gate. | repo fact |
| Branch deployed | `main`, **by default not by declaration** — `render.yaml` has no `branch:` key, so Render follows the repo's default branch | repo fact |
| Root directory | `system1-flask-chat` | `render.yaml:34` — **intended** |
| Auto-deploy | enabled (every push to `main`) | `render.yaml:44` — **intended** |
| Pre-deploy | `flask db upgrade` — migrations run before traffic shifts | `render.yaml:41` — **intended** |
| Health check | `/healthz` — runs `SELECT 1`, 503s if Postgres is unreachable | `routes.py` — **in the code** |
| Service URL | **unknown.** Derives from the service name, so it changes if the name does — settle the name before handing an address to a cohort. | repo fact |

> **The undeclared region is a latent defect, not just an unfilled cell.**
>
> Same-region Postgres is what makes the *internal* connection string usable; the
> external one needs a TLS handshake that flakes from inside Render's network.
> `render.yaml` pins no region on the web service or on either database, so an
> apply places all three at Render's default — and nothing in the file guarantees
> they land together. If the service and its database end up in different regions,
> `fromDatabase` hands over an internal host that the service cannot reach, and
> the failure looks like a connection timeout rather than a config error.
>
> Pin `region:` explicitly on all three before applying the Blueprint. Which
> region is a decision, not a default worth inheriting silently.

> **Rebuilt on Pro tier, 2026-07-29, rather than migrated.**
>
> The legacy free-tier database was gone before we decided anything: the
> 2026-07-29 logs show `failed to resolve host 'dpg-d84h9epkh4rs73d70pgg-a'`
> — *name resolution*, meaning the instance no longer existed. It was ~73
> days old against a 30-day rolling expiry.
>
> Starting from an empty database is also what let Alembic adopt the schema
> with no hand-run `flask db stamp head` against production (ADR-0006), which
> was the riskiest step in the original plan.
>
> The legacy service `srv-d84ha1og4nts73f73rng` is kept **suspended** as a
> control until the new stack is verified, which is why the new names carry a
> `-pro` suffix. Once it is deleted, renaming back to `teacherbot` is a
> one-line `render.yaml` change and a re-apply — but the URL changes with the
> name, so do that *before* handing an address to a cohort.

## First bootstrap (Blueprint)

The dashboard's Blueprint flow needs a payment method on file; Pro satisfies
that. One apply creates the web service, the database, and staging.

**1. Fill in the three `plan:` placeholders in `render.yaml`.** They are
deliberately invalid, so an unedited apply fails rather than silently
provisioning free tier and re-inheriting the expiry that deleted the last
database.

**2. Apply the Blueprint** — Render dashboard → New → Blueprint → this repo.

**3. Set the three `sync: false` secrets** on the service, or the deploy will
refuse to start (`create_app` raises, by design):
`ANTHROPIC_API_KEY`, `FLASK_SECRET_KEY`, `ADMIN_PASSWORD`.
`FLASK_APP` and `DATABASE_URL` come from the Blueprint.

**4. Verify, in this order** — each step catches a different failure:

```bash
# a. Migrations ran. On an empty database this is the first `flask db
#    upgrade`; no `stamp head` is needed, which is the point of rebuilding.
render logs --resources <srv-id> | grep -i alembic
#    expect: "Running upgrade  -> 69d2bbe0a8f9, baseline: ..."

# b. The database is actually reachable — NOT `/`, which renders the picker
#    from memory and returns 200 over a dead database (#38).
curl -sS -w '\n%{http_code}\n' https://<service>.onrender.com/healthz
#    expect: {"status":"ok","database":"ok"} and 200

# c. The path that touches Postgres without exception handling.
curl -sS -o /dev/null -w '%{http_code}\n' \
  -X POST -d 'password=<csc134 passcode>' \
  https://<service>.onrender.com/csc134/login
#    expect: 302 to /csc134/chat. A 500 means the schema is wrong.
```

**5. Record the service URL and IDs** in the tracking issue, and update the
table above.

If a name collides on apply, the legacy `teacherbot` service still exists —
suspend or rename it, or adjust the names in `render.yaml`.

## Required environment variables

| Variable | Source / how to set |
|---|---|
| `ANTHROPIC_API_KEY` | Instructor's key from https://console.anthropic.com/. Starts with `sk-ant-`. |
| `FLASK_SECRET_KEY` | Generated random hex: `python3 -c "import secrets; print(secrets.token_hex(32))"`. Rotate on suspected leak. |
| `ADMIN_PASSWORD` | Chosen string. Gates `/<slug>/admin?password=…` per skin (e.g. `/csc114/admin?password=…`). Alpha-grade auth — replace before public use. |
| `DATABASE_URL` | Connection string from the `teacherbot-pro-db` instance. Use the **internal** one — the external requires a TLS handshake that flakes from inside Render's network. `app.py` rewrites `postgres://` and `postgresql://` to `postgresql+psycopg://`. |
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
| `CTS285_USERNAME`, `CTS285_PASSWORD`, `CTS285_ACTIVE_MODULE`, `CTS285_TOKEN_BUDGET`, `CTS285_ANTHROPIC_API_KEY` | The `cts285` skin. Declared in `render.yaml` with no value. See "CTS 285 skin" below for each one, what a blank means, and the dedicated-workspace key. |
| `GROUP_TOKEN_BUDGET` | Per-cohort token ceiling for newly created groups (default 25,000,000). Existing rows are lifted to the default at next login by `Group.raise_budget_floor()`, because a column default only applies on INSERT. That workaround predates Alembic (ADR-0006) and is scheduled for removal when the budget moves to a seat (ADR-0004). Note this variable is **not** declared in `render.yaml`, so production runs on the 25M fallback. |

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

## CTS 285 skin (`/cts285/`)

The `cts285` skin is a Systems Analysis & Design tutor on `claude-haiku-5-5`
(ADR-0007). It is out of character, has a username and a password, and answers
from a vendored copy of the student-visible course pages. This section is the
operator's side of it.

**To test it before students use it, follow `docs/TESTING-CTS285.md`.** It runs
from the free test suite through a local run, the behaviour banks and a hand test
to the live checks below.

> **Every step marked `[credentials]` needs access this repository's authoring
> session did not have** (the Render dashboard or API, the Anthropic Console, a
> live API key). Nothing below was run against a live service. The commands
> that touch only a local database were run against a scratch SQLite database.
> Treat the rest as unverified until you have done each one once.

### Host: stay on Render

Keep this service on Render. The Blueprint (`render.yaml`), the
`preDeployCommand: flask db upgrade` migration step, the `/healthz` deploy gate
and the Postgres wiring already exist, and the repository tests the migration path
(`tests/test_migrations.py`) and the health check (`tests/test_healthz.py`). A different host means re-plumbing all four and gains nothing at
this traffic: the skin's estimated load is a few thousand short messages a
month. **Any plan price you see quoted anywhere, including in ADR-0007, comes
from outside this repository. Read it from the Render dashboard before you
choose a plan.**

### Step 0: establish what is live `[credentials]`

Do this first, and assume nothing. Follow "Service summary" above: the legacy
free-tier service and its database are gone, and the Blueprint has never been
applied. Find out from the Render dashboard whether any teacherbot service
exists, what plan and region it has, and what URL it serves. Record what you
find in the Service summary table, replacing the **intended** rows. If nothing
is live, do "First bootstrap (Blueprint)" first (fill in the three `plan:`
placeholders and pin `region:` on all three resources; both are your decisions,
and this section does not make them), then come back here.

### Environment variables for the skin

`render.yaml` declares all five with `sync: false` and no value. This
repository is public, so a credential is never written into it. All five are
optional: a variable that is unset **or blank** falls back to the skin's own
default, so a blank dashboard field cannot become the credential. `[credentials]`
for each.

| Variable | Set it to | If unset or blank |
|---|---|---|
| `CTS285_USERNAME` | The username students type. Case and surrounding spaces are ignored. | `CTS285` |
| `CTS285_PASSWORD` | The password students type. Exact match. | `algorithm` |
| `CTS285_ACTIVE_MODULE` | `m0` to `m8`: the module whose pages are in the prompt. | `m4` |
| `CTS285_TOKEN_BUDGET` | An integer below 2,147,483,647 (see "Budget" below). A larger or non-integer value stops the app at start, naming the variable. | 2,000,000,000 |
| `CTS285_ANTHROPIC_API_KEY` | A key from a dedicated Anthropic workspace (see below). | The skin answers on `ANTHROPIC_API_KEY`, which csc134 also uses. |

- **Rotate `CTS285_PASSWORD` away from `algorithm` before real students log
  in.** `algorithm` and `CTS285` are the documented test defaults, and both are
  published in this public repository. One shared username and password is all
  this skin has: there is no per-student identity (ADR-0007 Consequences, B20).
- **Use a dedicated Anthropic workspace key for `CTS285_ANTHROPIC_API_KEY`.**
  In the Anthropic Console, create a workspace for CTS 285, set a monthly spend
  limit on it, and create the key inside it. That is what keeps this skin's
  spend, and its prompt-cache namespace, apart from csc134. If you leave the
  variable unset, **nothing fails**: the skin answers on the shared key and the
  spend lands on the shared credits. That is deliberate, and it is also silent,
  so check the Console after the first message to see which workspace was billed.
- The skin reads these when the service starts, so a change needs the service to
  restart or redeploy (Render normally does that when you save an environment
  variable; confirm it in the dashboard). A value that resolves to
  no corpus directory is logged and ignored, and the skin keeps `m4`.
- Read or update them with the REST calls in "Optional environment variables"
  above. Check Render's API reference before you use the `PUT` form with a single
  key: it may replace the whole list, and the example above sends one variable.
  The dashboard is the safer route.

### Budget

`CTS285_TOKEN_BUDGET` is a circuit breaker for the whole cohort, counted the way
`claude_handler._usage_total` counts (cache reads at full weight, K10). A message
counts about 44,000 tokens because the cached module window is counted every time,
so the 2,000,000,000 default is roughly 45,000 messages. It is below the int4 column
limit, so no migration is involved.

- **The budget is raise-only.** `do_login` lifts an existing group to the skin's
  budget and never lowers it. Raising `CTS285_TOKEN_BUDGET` takes effect at the
  next login. **Lowering it does not touch a group that already exists.** To
  lower it, also set `g.token_budget` in the shell below.
- `tokens_used` stops at the budget and the student sees "Token budget exhausted.
  Contact your instructor." There is no admin control for this skin's budget.

**Monthly reset `[credentials]`.** Open a shell on the Render service (dashboard,
Shell tab), `cd` to the app root (`system1-flask-chat`) if it did not start there,
and run:

```bash
python - <<'PY'
from app import create_app
from models import db, Group

with create_app().app_context():
    g = Group.query.filter_by(name='cts285').first()
    g.tokens_used = 0
    db.session.commit()
    print('tokens_used', g.tokens_used, 'of', g.token_budget)
PY
```

It prints `tokens_used 0 of <budget>`. If it fails with `AttributeError:
'NoneType' ...`, no one has logged in to the skin yet and there is nothing to
reset. This changes the counter only. It deletes no transcript.

### Re-syncing the corpus

The corpus under `system1-flask-chat/context/cts285/` is a committed copy of the
course's student-visible pages. The upstream repository is private, so the sync
reads a local clone and never clones over the network. Run it from a machine that
has the clone. It needs no Render access.

```bash
# 1. In the CTS-285 clone: be on the commit you mean to vendor, with a clean tree
#    under every manifest path (the sync refuses a dirty one, so the recorded SHA
#    is true).
git -C /path/to/cts-285_SOURCE status --short

# 2. In this repository, on a branch (never main):
python scripts/sync_course_corpus.py \
  --manifest scripts/cts285_manifest.yaml \
  --source /path/to/cts-285_SOURCE

# 3. Read the diff. context/cts285/_provenance.txt must show the SHA you expect.
git status --short && git diff --stat

# 4. Run the suite. The deny-list test reads the vendored files on disk.
python -m pytest -q

# 5. Commit, open a PR, merge.
```

- **The sync only vendors files listed in `scripts/cts285_manifest.yaml`.** A page
  added upstream is not vendored until someone adds it to `paths`. To add one,
  edit the manifest, re-run, and let the deny guard judge it: a path under
  `build-guides/`, `instructor-guides/`, `planning/`, `review-target/`,
  `assignments/` and the other denied locations makes the sync raise and write nothing.
  If it raises, the allow-list is wrong. Do not weaken `deny:` to get past it.
- **Merging to `main` deploys** (`autoDeploy: true`). The prompt changes on that
  deploy, so the first message after it writes a new cache entry.
- **This repository is public, so the vendored pages are public.** They are
  material students already see in Canvas. The instructional lead should confirm
  that publishing it here is acceptable before the first sync with new pages.
- The tutor describes the source repository's version of each page. A live Canvas
  page can differ. `context/cts285_context.md` tells the tutor to believe the page
  the student sees.

### Verification after a deploy `[credentials]`

Replace `<service>` with the real host. Do these in order. Each step catches a
different failure.

```bash
# a. The database is reachable. NOT `/`, which returns 200 over a dead database.
curl -sS -w '\n%{http_code}\n' https://<service>/healthz
#    expect: {"status":"ok","database":"ok"} and 200

# b. Login with the username AND the password. Use the values you set,
#    or CTS285 / algorithm if you set none.
curl -sS -c /tmp/cts285.jar -o /dev/null -w '%{http_code} %{redirect_url}\n' \
  -d 'username=CTS285' -d 'password=algorithm' \
  https://<service>/cts285/login
#    expect: 302 and a redirect to .../cts285/chat
#    A wrong username or password returns 200 (the login page again) and no cookie.
#    A 500 means the schema or DATABASE_URL is wrong.

# c. One chat message.
curl -sS -b /tmp/cts285.jar -H 'Content-Type: application/json' \
  -d '{"message":"Which module owns the step from evidence to requirement?","history":[]}' \
  https://<service>/cts285/api/chat
#    expect: JSON with a non-empty "response" and a "tokens_remaining" number.
#    502 with "The tutor is unavailable right now" means the API call failed:
#    check the key, the model name and the workspace spend limit in the Console.
```

**d. Confirm the prompt cache is working.** The first message writes the cache
entry and the second reads it. The app does not log usage, and the budget counter
cannot show this, because it counts a cache read at full weight, so a miss and a hit
give the same number. Use either of these:

- In the Anthropic Console, open the CTS 285 workspace usage view after the second
  message and look for cache-read tokens that are greater than zero.
- Or run this in a shell on the service. It makes two real API calls (a few
  tenths of a cent) through the same code path the app uses, and prints the cache
  counters from each.

```bash
python - <<'PY'
from auth import SKINS, load_skin_context, load_skin_notes, load_skin_persona
import claude_handler as ch

s = SKINS['cts285']
system = ch._system_blocks(load_skin_context('cts285'),
                           load_skin_persona('cts285'), load_skin_notes('cts285'))
for q in ('Which module owns Evidence to Requirement?', 'Name the chain.'):
    kw = ch._request_kwargs(s['model'], s['max_tokens'], s['request_options'],
                            system, [{'role': 'user', 'content': q}])
    u = ch._client_for(s['api_key_env']).messages.create(**kw).usage
    print('cache_creation', u.cache_creation_input_tokens,
          'cache_read', u.cache_read_input_tokens)
PY
```

Expect `cache_read 0` on the first line and `cache_read` greater than zero on the
second. If both lines show `cache_read 0` and `cache_creation 0`, the prefix is
below the model's cache minimum or is changing between calls, and every message is
billing in full. Do not hand the address to a cohort until this shows a read.

Also check, in the Console, that the usage appeared under the **CTS 285 workspace**
and not the shared one. If it did not, `CTS285_ANTHROPIC_API_KEY` is unset or blank
on the service.

### Unverified here

These come from the repository, not from a live service. Check each before you
rely on it:

- The Haiku 5.5 rates, cache minimum and tokenizer ratio behind ADR-0007's cost
  figures. ADR-0007 says they came from a bundled reference and were not checked
  against the live pricing page. Re-read them in the Console.
- That `output_config.effort` and the bare model name `claude-haiku-5-5` are
  accepted by the live API. No test calls the API: the `live` tests are deselected,
  and `tests/test_live_anthropic.py` names no `cts285` skin.
- That Render accepts an empty value for a `sync: false` variable when you apply
  the Blueprint. The code treats a blank as unset. If the dashboard insists on a
  value, enter the default shown in the table above.
- `/cts285/admin` exists like the other skins' admin pages and takes
  `?password=<ADMIN_PASSWORD>` in the URL (B4, #26). That is the service-wide admin
  password, not `CTS285_PASSWORD`.

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
# Internal connection string for teacherbot-pro-db-staging
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
`../docs/historical/plans/2026-05-16-render-deployment.md` still works and is
the fallback if the Blueprint flow is unavailable.

The real smoke test after any deploy is a `/csc134/` login (or, for the cts285 skin, the
username-and-password login in "CTS 285 skin" above): `do_login` queries
the database without exception handling, so it is the path that fails loudly if
the schema or connection string is wrong. `/` renders without touching the
database and will happily return 200 over a broken one.

<!-- deploy verified 2026-05-17T01:46:44Z -->
