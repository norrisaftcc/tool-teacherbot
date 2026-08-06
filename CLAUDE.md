# AlgoCratic TA Systems

A Flask AI teaching assistant serving one **skin** per cohort, deployed to
Render — though what is running there right now is unverified, and establishing
that is a prerequisite for most operational work (see **Live service**).
System 2 (the CLI distribution in the original plan) was never started and its
directory does not exist — see `docs/historical/`.

## Read these first

| File | Why |
|---|---|
| `docs/registry/KEEP.md` | **Decision register.** What is frozen, what is still negotiating, and the backlog. Start here. K18 is the operative rule on what code the bot may quote — it is narrower than the persona's "never hand over a solution" reads, and `evals/csc134/m1.yaml` item `m1-03` guards it. |
| `docs/adr/` | Why the code is shaped this way. 0001-0004 and 0006 Accepted, 0005 Proposed. Each ADR's own header is authoritative; `docs/adr/README.md`'s index column is a copy and has drifted before. |
| `system1-flask-chat/DEPLOY.md` | Operator runbook — env vars, redeploy, logs, rollback, suspend. |

## What's where

| Path | Purpose |
|---|---|
| `system1-flask-chat/app.py` | The factory. `_require_secrets` (no fallbacks, raises at startup), and the `TESTING` gate on `db.create_all()`. |
| `system1-flask-chat/auth.py` | `SKINS` registry — passcode, model, persona, corpus window per cohort. Also the path-traversal/symlink guard. |
| `system1-flask-chat/models.py` | `Group` / `Conversation` / `Message`, and `increment_tokens` (#28). |
| `system1-flask-chat/migrations/` | Alembic. Owns the real schema (ADR-0006). One revision so far — baseline `69d2bbe0a8f9`. |
| `system1-flask-chat/routes.py` | Root picker + `skin_blueprint(slug)` factory. Login, chat, SSE stream, admin, per skin. |
| `system1-flask-chat/claude_handler.py` | Prompt composition, 1h ephemeral cache block, `_usage_total` token accounting. |
| `system1-flask-chat/context/` | Personas, cohort headers, teaching notes, and vendored corpora. |
| `scripts/sync_course_corpus.py` | Vendors a course repo into `context/<slug>/` per a manifest. Manifests are `scripts/csc114_manifest.yaml` and `csc134_manifest.yaml`; the script defaults to the **csc114** one, so `--manifest` is mandatory in practice. |
| `scripts/eval_persona.py` | Runs a behaviour bank against the real composed prompt. |
| `scripts/export_group_transcripts.py` | Exports a cohort's transcripts before its skin is unregistered (K12). |
| `evals/csc134/m0.yaml`, `m1.yaml` | The behaviour banks. csc134 only, m0 and m1. |
| `.github/workflows/` | `tests.yml` runs both suites on every PR and push to `main`, pinned to `.python-version` so CI and Render agree. `live.yml` runs the paid `live` tests on manual dispatch plus a weekly schedule. |
| `docs/historical/` | Every superseded planning doc, bannered. Do not act on them. `plans/` and `specs/` are the May 2026 *executable* plans, written as task-by-task steps against a free-tier stack that no longer exists. Their agent-mandate directives were struck under K19. |

## Live service

- **Push to `main` auto-deploys** (~1 min to live), `rootDir: system1-flask-chat`
- **What is actually deployed is currently unknown to this repo.** `srv-d84ha1og4nts73f73rng` / `dpg-d84h9epkh4rs73d70pgg-a` are the *old free-tier* IDs and the database is **gone**, not stale — `DEPLOY.md` records `failed to resolve host`, which is name resolution. The Pro stack in `render.yaml` has never been applied: its three `plan:` values are still the deliberately-invalid placeholders. Establish the real state and record it in `DEPLOY.md` before doing anything that assumes production exists.
- Render CLI workspace: `render workspace set tea-d81rjp0sfn5c738tl430` (once per shell)

## Commands

```bash
python -m pytest -q                    # both suites, from the repo root
python scripts/eval_persona.py --skin csc134 --module m0 --backend anthropic --runs 3
python scripts/sync_course_corpus.py --manifest scripts/csc134_manifest.yaml
```

CI runs the same `pytest` on every PR, so a green local run is the same evidence
CI will produce. `--runs N` samples each eval item N times; three is the smallest
N that separates always / never / sometimes, and an item clean twice and flagged
once prints `VARY` rather than rounding to a neighbour (#44). It is still not a
gate — K16 wants a rate *and* a byte-exact pass condition, and this is half.

## Gotchas

### Schema — read before touching models.py

**Alembic owns the production schema** (ADR-0006). `db.create_all()` still exists
but runs only under `TESTING`. Never let both touch a real database: `create_all`
writes no `alembic_version` row, so a table it builds is invisible to Alembic and
the next migration fails on a table that already exists.

Edit a model, generate a migration:

```bash
cd system1-flask-chat && flask db migrate -m "what changed and why"
```

Then **read the generated file** — autogenerate misses server defaults, sees a
rename as drop+add, and skips CHECK constraints. `tests/test_migrations.py` fails
CI when models and migrations disagree, which is what replaced the old blanket
prohibition (K6, superseded). Rehearse on `teacherbot-pro-db-staging` before
merging: the suite runs on SQLite, which accepts things Postgres rejects. An
empty staging database only proves the DDL parses — seed it with representative
rows first, or the rehearsal returns green and is evidence of nothing.

### Repo

- **Root `runtime.txt` is invisible to Render** because `rootDir: system1-flask-chat`. The version comes from `system1-flask-chat/.python-version`. Don't add a second mechanism.
- **`pytest.ini` needs `--import-mode=importlib`.** Both test suites are packages named `tests`; without it, collection dies on duplicate module names.
- **Two test suites, two import roots.** `pytest.ini` handles both — run `pytest` from the repo root. Because both are named `tests`, always write test paths **qualified**: `system1-flask-chat/tests/test_auth.py`, not `tests/test_auth.py`. Nearly every test named in this file lives in the app suite.
- **`pytest.ini` also carries `-m "not live"`**, and that is what keeps a bare `pytest` free. Tests marked `live` call the real Anthropic API and cost money; they are opted into with `pytest -m live` and CI runs them only from `live.yml`. Deselecting by default rather than by convention means a `live` test added later cannot start spending on every PR.

### Prompt composition

- **The corpus is windowed** (ADR-0002): `corpus_index` + one `active_module`. Never load the whole corpus; that is what the window exists to prevent.
- **The model is per-skin, not global.** `claude_handler.py`'s `MODEL = 'claude-sonnet-4-6'` is only a fallback; `auth.py` gives csc134 `claude-haiku-4-5-20251001` and csc114 Sonnet. The cache floor below therefore binds **only** the Haiku skin.
- **Haiku will not cache a prefix under 4096 tokens** — silently, no error. `system1-flask-chat/tests/test_auth.py` guards every csc134 window against that floor; the thinnest clear it by **610** (m3), 949 (m5), 1011 (m7) and 1162 (m6) tokens. Any corpus trimming will trip it, and that is the test doing its job. Note the guard composes *without* teaching notes while production sends them, so it measures ~745 tokens less than the real prefix — conservative in direction, but it means the guard is blind to `_system_blocks`, which is where the cached block is actually built.
- **The cached prefix must stay byte-stable across every seat in a cohort.** That is what makes one cache entry serve the whole class; a per-seat byte in the cached block gives every seat its own entry, and 1h writes bill at ~2x against reads at ~0.1x. **Nothing guards this**, and nothing will report it either: `_usage_total` counts cache reads at full weight, so a miss and a hit produce the identical number. Only the invoice moves. That accounting is **frozen** (K10) rather than pending — correct as a token count, wrong as a cost proxy.
- **Context is reloaded per request, never cached in the session** — a window is tens of KB and the signed cookie limit is 4KB. `system1-flask-chat/tests/test_skins.py` guards this.
- **Hoist what the SSE generator needs before `generate()`** — but not for the reason the code used to give. `routes.py` wraps the generator in `stream_with_context`, so the request context *is* alive inside it: `session`, `request` and the DB all work. The real constraint is that returning `Response()` commits the status line, so nothing inside `generate()` can emit a 403 or 409, and `session` mutations never reach a cookie. Do budget and auth checks *before* the response, or a rejection becomes an SSE error event instead of a status code.

### Render

- **`/healthz` is the deploy gate. `/` is a false positive.** `/` renders the picker from the in-memory `SKINS` dict and returns 200 over a database that does not exist — that is exactly how the legacy service reported healthy on 2026-07-29 while every login 500'd (#38). `healthCheckPath: /healthz` runs `SELECT 1` and 503s, so a mis-linked `DATABASE_URL` or a failed migration fails the deploy instead of going live broken. Never health-check this app at `/`.
- **Same-region Postgres needs the internal connection string.** The external one requires a TLS handshake that flakes from inside Render's network.
- **`render.yaml` pins no `region:`** on the web service or on either database, so an apply takes Render's default and nothing guarantees the three land together. A split placement hands `fromDatabase` an internal host the service cannot reach, and it presents as a connection *timeout* rather than a config error — which is why it is worth knowing before you debug it. Pin all three before applying the Blueprint; which region is an open decision (B16).
- **The secret is `FLASK_SECRET_KEY`, not `SECRET_KEY`.** `create_app()` raises at startup if it or `ADMIN_PASSWORD` is missing — deliberately no fallbacks, since the old values are published in this public repo. Note K7 in the register calls it `SECRET_KEY` and is wrong.
- **Render CLI v2.17.0 cannot create Postgres or delete services.** Use the REST API for those two.
- **`render --output json` emits ANSI escapes when stdout isn't a TTY**, which breaks jq. Use the REST API when scripting.
- **Pro tier since 2026-07-29.** The stack was rebuilt rather than migrated — the old free-tier Postgres (`srv-d84ha1og4nts73f73rng`) carried a 30-day rolling expiry and was ~73 days old. Starting empty is also what let Alembic adopt the schema without a hand-run `stamp head` against production.
- **The Blueprint is now the canonical bootstrap.** The dashboard flow needs a payment method on file; Pro satisfies that. The three `plan:` values in `render.yaml` are deliberately invalid placeholders so an unedited apply fails loudly instead of provisioning free tier.
- **`preDeployCommand: flask db upgrade`** runs migrations before traffic shifts. A failed migration blocks the deploy and leaves the old version serving — fix forward, don't roll the service back.
- **`FLASK_APP=app:create_app` is required in the environment**, or the pre-deploy command fails before the app starts.

### Known open defects

All tracked as issues and indexed in `docs/registry/KEEP.md`. The live ones worth
knowing before you touch related code: admin auth is a query parameter (#26), no
CSRF (#27), `increment_tokens` has a read-modify-write race (#28), test deps ship
to production (#31), corpus manifests track a moving branch (#24 — a declared
prerequisite for ADR-0005).

**Before citing this list, check it.** It named `marked` as unpinned (#25) for
eight days after #41 vendored `marked@18.0.7` and dropped the CDN tag. Verify
against `KEEP.md`'s backlog and `gh issue view`, not against this paragraph.

## Tech stack

Flask 3.0.0, Flask-SQLAlchemy 3.1.1, Flask-Migrate 4.1.0, Anthropic SDK 0.101.0,
psycopg3, gunicorn 21.2.0, Python 3.11.9 (from `system1-flask-chat/.python-version`).

**Render tier, stated precisely, because two shorter versions are both wrong.**
The *account* is Pro (since 2026-07-29). The *service plans* are unset — the
three `plan:` values in `render.yaml` are still invalid placeholders — so
nothing is provisioned under them. Neither "free tier" nor "running on Pro" is
an accurate summary.

## Conventions

- **Branch:** `<slug>/feature-name`, e.g. `csc134/pair-assignments-with-modules`.
- **Open a PR** for non-trivial changes even when solo — it keeps a reviewable record.
- **Commit bodies explain why, at length**, and name what is uncertain rather than papering over it. Match that register; it is the most valuable documentation in this repo.
- **A decision that isn't written down doesn't exist.** Frozen and negotiating entries go in `docs/registry/KEEP.md`; anything that constrains the schema or the prompt gets an ADR.
- **Closing an issue is half the change. Striking its register row is the other half.** This repo's recurring failure is not wrong documentation, it is *fixes that never propagate back* — B3 and B10 both stayed listed as open work after shipping, ADR-0004 and 0006 were built on while their index still read `Proposed`, and this file spent eight days pointing at a solved defect. When you fix something, grep for what asserts the old state before you open the PR. B17 proposes making that a check instead of a habit.
