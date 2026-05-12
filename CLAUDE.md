# AlgoCratic TA Systems

Planning and bootstrap repository for a dual-system AI-assisted capstone education platform.

## Current State

**This repo is documentation/planning only** — no implementation code exists yet.
Actual system code will be built inside subdirectories by two parallel Claude Code instances.

## What Gets Built

- **System 1** (`system1-flask-chat/`): Flask web chat with student auth, per-group context injection, conversation logging → deployed to Render
- **System 2** (`system2-code-distribution/`): CLI distribution framework — API key packaging, CLAUDE.md templates with pedagogical guardrails, `setup.py` for generating per-group configs

## Key Files

| File | Purpose |
|------|---------|
| `HANDOFF.md` | Launch instructions for both instances (read this first) |
| `TA_SYSTEMS_PARALLEL_PLAN.md` | Complete technical spec (25KB) |
| `SYSTEM1_CLAUDE.md` | Copy to `system1-flask-chat/CLAUDE.md` before launching Instance A |
| `SYSTEM2_CLAUDE.md` | Copy to `system2-code-distribution/CLAUDE.md` before launching Instance B |
| `README.md` | Student/instructor-facing overview |

## Launch Parallel Development

```bash
# Copy CLAUDE.md guides into place
cp SYSTEM1_CLAUDE.md system1-flask-chat/CLAUDE.md
cp SYSTEM2_CLAUDE.md system2-code-distribution/CLAUDE.md

# Terminal 1: Instance A (System 1 - Flask Chat)
cd system1-flask-chat && claude

# Terminal 2: Instance B (System 2 - Distribution)
cd system2-code-distribution && claude
```

## Architecture

```
System 1 (Flask + PostgreSQL on Render)
  Student login → group context injection → Claude API → conversation log

System 2 (CLI distribution)
  setup.py → per-group folders (API key + spend_cap.json + CLAUDE.md)
```

## Gotchas

- Subdirectories `system1-flask-chat/`, `system2-code-distribution/`, `shared/` don't exist yet — instances create them
- `SYSTEM1_CLAUDE.md` / `SYSTEM2_CLAUDE.md` are NOT root-level CLAUDE.md files; they go in subdirs
- Branch naming convention: `system1/feature-name` and `system2/feature-name`
- Shared files in `shared/` require PR + cross-instance approval before merging

## Tech Stack

- System 1: Flask 3.x, Flask-Login, Flask-SQLAlchemy, Anthropic SDK, SQLite→PostgreSQL, Render
- System 2: Python 3.11+, argparse, pathlib (no external deps by design)
- Shared context format: `group_N_context.md` files (Instance A defines format, Instance B adopts it)
