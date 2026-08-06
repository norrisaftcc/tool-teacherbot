# AlgoCratic TA Systems

A Flask AI teaching assistant serving one **skin** per cohort, deployed to
Render — though what is running there right now is unverified, and establishing
that is a prerequisite for most operational work (see **Live service**).
System 2 (the CLI distribution in the original plan) was never started and its
directory does not exist — see `docs/historical/`.

## Read these first

| File | Why |
|---|---|
| `docs/registry/KEEP.md` | **Decision register.** What is frozen, what is still negotiating, and the backlog. Start here. |
| `docs/adr/` | Why the code is shaped this way. 0001-0004 and 0006 Accepted, 0005 Proposed. |
| `system1-flask-chat/DEPLOY.md` | Operator runbook — env vars, redeploy, logs, rollback, suspend. |

## What's where

| Path | Purpose |
|---|---|
| `system1-flask-chat/auth.py` | `SKINS` registry — passcode, model, persona, corpus window per cohort. Also the path-traversal/symlink guard. |
| `system1-flask-chat/routes.py` | Root picker + `skin_blueprint(slug)` factory. Login, chat, SSE stream, admin, per skin. |
| `system1-flask-chat/claude_handler.py` | Prompt composition, 1h ephemeral cache block, `_usage_total` token accounting. |
| `system1-flask-chat/context/` | Personas, cohort headers, teaching notes, and vendored corpora. |
| `scripts/sync_course_corpus.py` | Vendors a course repo into `context/<slug>/` per a manifest. |
| `scripts/eval_persona.py` | Runs a behaviour bank against the real composed prompt. |
| `scripts/export_group_transcripts.py` | Exports a cohort's transcripts before its skin is unregistered (K12). |
| `evals/csc134/m0.yaml`, `m1.yaml` | The behaviour banks. csc134 only, m0 and m1. |
| `docs/historical/` | Every superseded planning doc, bannered. Do not act on them. `plans/` and `specs/` are the May 2026 *executable* plans, written as task-by-task steps against a free-tier stack that no longer exists. Their agent-mandate directives were struck under K19. |

## Live service

- **Push to `main` auto-deploys** (~1 min to live), `rootDir: system1-flask-chat`
- **What is actually deployed is currently unknown to this repo.** `srv-d84ha1og4nts73f73rng` / `dpg-d84h9epkh4rs73d70pgg-a` are the *old free-tier* IDs and the database is **gone**, not stale — `DEPLOY.md` records `failed to resolve host`, which is name resolution. The Pro stack in `render.yaml` has never been applied: its three `plan:` values are still the deliberately-invalid placeholders. Establish the real state and record it in `DEPLOY.md` before doing anything that assumes production exists.
- Render CLI workspace: `render workspace set tea-d81rjp0sfn5c738tl430` (once per shell)

## Commands

```bash
python -m pytest -q                    # both suites, from the repo root
python scripts/eval_persona.py --skin csc134 --module m0 --backend anthropic
python scripts/sync_course_corpus.py --manifest scripts/csc134_manifest.yaml
```

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
- **Two test suites, two import roots.** `pytest.ini` handles both — run `pytest` from the repo root.

### Prompt composition

- **The corpus is windowed** (ADR-0002): `corpus_index` + one `active_module`. Never load the whole corpus; that is what the window exists to prevent.
- **Haiku will not cache a prefix under 4096 tokens** — silently, no error. `test_auth.py` guards every csc134 window against that floor, and the thinnest (m3) clears it by **610** tokens. Any corpus trimming will trip it, and that is the test doing its job. Note the guard composes *without* teaching notes while production sends them, so it measures ~745 tokens less than the real prefix — conservative in direction, but it means the guard is blind to `_system_blocks`, which is where the cached block is actually built.
- **The cached prefix must stay byte-stable across every seat in a cohort.** That is what makes one cache entry serve the whole class; a per-seat byte in the cached block gives every seat its own entry, and 1h writes bill at ~2x against reads at ~0.1x. **Nothing guards this** — and `_usage_total` counts cache reads at full weight, so a cache miss and a cache hit report the identical number. Only the invoice moves.
- **`_usage_total` counts cache reads at full weight.** Correct as a token count, wrong as a cost proxy, and **frozen that way** (K10) rather than pending.
- **Context is reloaded per request, never cached in the session** — a window is tens of KB and the signed cookie limit is 4KB. `test_skins.py` guards this.
- **Hoist what the SSE generator needs before `generate()`** — but not for the reason the code used to give. `routes.py` wraps the generator in `stream_with_context`, so the request context *is* alive inside it: `session`, `request` and the DB all work. The real constraint is that returning `Response()` commits the status line, so nothing inside `generate()` can emit a 403 or 409, and `session` mutations never reach a cookie. Do budget and auth checks *before* the response, or a rejection becomes an SSE error event instead of a status code.

### Render

- **Same-region Postgres needs the internal connection string.** The external one requires a TLS handshake that flakes from inside Render's network.
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
