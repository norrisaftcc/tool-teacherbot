# AlgoCratic TA Systems

A Flask AI teaching assistant, live on Render, serving one **skin** per cohort.
System 2 (the CLI distribution in the original plan) was never started and its
directory does not exist — see `docs/historical/`.

## Read these first

| File | Why |
|---|---|
| `docs/registry/KEEP.md` | **Decision register.** What is frozen, what is still negotiating, and the backlog. Start here. |
| `docs/adr/` | Why the code is shaped this way. 0001-0003 Accepted, 0004-0005 Proposed. |
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
| `evals/csc134/m0.yaml` | The only behaviour bank so far. |
| `docs/historical/` | Superseded planning docs. Bannered, do not act on them. |

## Live service

- **Push to `main` auto-deploys** (~1 min to live), `rootDir: system1-flask-chat`
- Service `srv-d84ha1og4nts73f73rng` · DB `dpg-d84h9epkh4rs73d70pgg-a` · virginia · free plan
- Render CLI workspace: `render workspace set tea-d81rjp0sfn5c738tl430` (once per shell)

## Commands

```bash
python -m pytest -q                    # both suites, from the repo root
python scripts/eval_persona.py --skin csc134 --module m0 --backend anthropic
python scripts/sync_course_corpus.py --manifest scripts/csc134_manifest.yaml
```

## Gotchas

### Schema — read before touching models.py

**`db.create_all()` creates missing tables and nothing else.** There is no
Alembic and no Flask-Migrate. Adding a **table** is free on the next deploy.
Adding a **column to an existing table** silently does nothing on deploy, and
then every query naming it raises `UndefinedColumn` in production. Tests cannot
catch it — they run on in-memory SQLite, which builds the schema fresh each run.
This is frozen entry K6, and ADR-0004 is designed around it.

### Repo

- **Root `runtime.txt` is invisible to Render** because `rootDir: system1-flask-chat`. The version comes from `system1-flask-chat/.python-version`. Don't add a second mechanism.
- **`pytest.ini` needs `--import-mode=importlib`.** Both test suites are packages named `tests`; without it, collection dies on duplicate module names.
- **Two test suites, two import roots.** `pytest.ini` handles both — run `pytest` from the repo root.

### Prompt composition

- **The corpus is windowed** (ADR-0002): `corpus_index` + one `active_module`. Never load the whole corpus; that is what the window exists to prevent.
- **Haiku will not cache a prefix under 4096 tokens** — silently, no error. `test_auth.py` guards every csc134 window against that floor, and the thinnest clear it by 163 tokens. Any corpus trimming will trip it, and that is the test doing its job.
- **`_usage_total` counts cache reads at full weight.** Correct as a token count, wrong as a cost proxy. Don't "fix" it into a cost estimate without deciding K10 first.
- **Context is reloaded per request, never cached in the session** — a window is tens of KB and the signed cookie limit is 4KB. `test_skins.py` guards this.
- **The SSE generator body runs after the request context is torn down.** Read anything you need from the app or DB *before* `generate()`.

### Render

- **Same-region Postgres needs the internal connection string.** The external one requires a TLS handshake that flakes from inside Render's network.
- **Render CLI v2.17.0 cannot create Postgres or delete services.** Use the REST API for those two.
- **`render --output json` emits ANSI escapes when stdout isn't a TTY**, which breaks jq. Use the REST API when scripting.
- **Free-tier Postgres has a 30-day rolling expiry**, one per workspace.
- **Blueprint apply via the dashboard requires payment info on file.** The CLI+REST path doesn't.

### Known open defects

All tracked as issues and indexed in `docs/registry/KEEP.md`. The live ones worth
knowing before you touch related code: admin auth is a query parameter (#26), no
CSRF (#27), `increment_tokens` has a read-modify-write race (#28), `marked` is
unpinned and unhashed (#25), corpus manifests track a moving branch (#24).

## Tech stack

Flask 3.x, Flask-SQLAlchemy, Anthropic SDK 0.101.0, psycopg3, gunicorn,
Python 3.11.9, Render free tier.

## Conventions

- **Branch:** `<slug>/feature-name`, e.g. `csc134/pair-assignments-with-modules`.
- **Open a PR** for non-trivial changes even when solo — it keeps a reviewable record.
- **Commit bodies explain why, at length**, and name what is uncertain rather than papering over it. Match that register; it is the most valuable documentation in this repo.
- **A decision that isn't written down doesn't exist.** Frozen and negotiating entries go in `docs/registry/KEEP.md`; anything that constrains the schema or the prompt gets an ADR.
