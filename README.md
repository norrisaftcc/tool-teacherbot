# AlgoCratic TA Systems

An AI teaching assistant for community-college courses. One Flask app serves a
**skin** per cohort: its own URL prefix, passcode, model, persona, and vendored
course corpus. Live on Render at https://teacherbot-6yut.onrender.com/.

> **Status, 2026-08-06.** CSC 114 has finished; its skin is still registered
> pending [#21](https://github.com/norrisaftcc/tool-teacherbot/issues/21). CSC 134
> is a Fall cohort. The capstone this was originally built for is weeks off. Its
> memory design,
> [ADR-0004](docs/adr/0004-identity-memory-and-the-session-boundary.md), was
> **Accepted** on 2026-07-29 and is not yet built
> ([#20](https://github.com/norrisaftcc/tool-teacherbot/issues/20)); the csc114
> repoint, [ADR-0005](docs/adr/0005-repoint-the-csc114-slot-to-the-prompt-wizard.md),
> is still **Proposed** and is the one open architectural question.
>
> The "System 2" CLI distribution described in the original plan was never
> started, and there is no `system2-code-distribution/` directory. Those
> documents are in [`docs/historical/`](docs/historical/).

## What it does

A student opens `/<slug>/`, enters the cohort passcode, and chats. Their messages
go to Claude with a system prompt composed of three parts that change on
different clocks:

| Part | Source | Changes |
|---|---|---|
| Persona | `context/<slug>_persona.md` | Rarely. Voice and pedagogical rules. |
| Teaching notes | `context/<slug>_teaching_notes.md` | Per course. Always on. |
| Course context | `context/<slug>_context.md` + windowed corpus | Per module. |

The corpus is **windowed**: only an always-on index plus the one active module
reaches the prompt. The full CSC 134 corpus is ~424 KB (~106k tokens) and stays
on disk; a window is ~5–27k. That is
[ADR-0002](docs/adr/0002-per-skin-persona-and-windowed-corpus.md), and it exists
because an earlier draft sent the whole corpus on every message.

The composed prompt goes out as a single cached block with a 1h TTL, so a whole
cohort shares one cache entry. Advance the week by setting
`<SLUG>_ACTIVE_MODULE` in the Render dashboard — no commit needed.

## Skins

| Slug | Course | Model | Status |
|---|---|---|---|
| `csc114` | Fundamentals of AI/ML | Sonnet | Finished. Being repointed — [#21](https://github.com/norrisaftcc/tool-teacherbot/issues/21) |
| `csc134` | Introduction to Programming (C++) | Haiku 4.5 | Fall 2026 |

Passcodes are not published here. `csc134`'s is overridable via `CSC134_PASSCODE`
so it can be rotated without a public commit.

## Layout

```
system1-flask-chat/        the app (Render rootDir)
  app.py                   factory; db.create_all() only under TESTING
  auth.py                  SKINS registry, corpus windowing, path-traversal guard
  routes.py                picker + one blueprint per skin
  claude_handler.py        prompt composition, caching, token accounting
  models.py                Group / Conversation / Message
  migrations/              Alembic — owns the real schema (ADR-0006)
  context/                 personas, headers, vendored corpora
  DEPLOY.md                operator runbook — env vars, logs, rollback
docs/adr/                  architecture decisions (0001-0006)
docs/registry/KEEP.md      decision register + backlog
docs/historical/           superseded planning docs, kept as paper trail
scripts/                   corpus sync, eval harness, transcript export
evals/                     behaviour banks
tests/                     tests for scripts/
```

## Running it locally

```bash
cd system1-flask-chat
cp .env.example .env          # then fill it in
pip install -r requirements.txt
flask --app app:create_app run --debug
```

`FLASK_SECRET_KEY` and `ADMIN_PASSWORD` have no fallbacks — a missing one raises
at startup rather than silently signing session cookies with a value published in
this repo. SQLite is used automatically when `DATABASE_URL` is unset, so local
development needs no Postgres.

## Tests

```bash
python -m pytest -q          # both suites, from the repo root
```

`pytest.ini` handles the two import roots; the comment in it explains why
`--import-mode=importlib` is load-bearing. CI runs the same command on every PR.

## Evals

Behaviour banks check the *bot*, not the student. Each item is a message a real
student might send, and the pass condition is what the bot must and must not do
with it.

```bash
python scripts/eval_persona.py --skin csc134 --module m0 --backend ollama
python scripts/eval_persona.py --skin csc134 --module m0 --backend anthropic
```

Only the Anthropic run decides anything
([ADR-0003](docs/adr/0003-local-model-backend-for-dev-and-eval.md)); the Ollama
run narrows the search for free. The flags are mechanical triage, not a grader —
a human reads the transcripts.

## Deploying

Push to `main`. Render auto-deploys from it with `rootDir: system1-flask-chat`.
Env vars, log tailing, rollback and suspend are in
[`system1-flask-chat/DEPLOY.md`](system1-flask-chat/DEPLOY.md).

## Where to look first

- **What's decided and what isn't:** [`docs/registry/KEEP.md`](docs/registry/KEEP.md)
- **Why the code is shaped this way:** [`docs/adr/`](docs/adr/)
- **How to operate it:** [`system1-flask-chat/DEPLOY.md`](system1-flask-chat/DEPLOY.md)
