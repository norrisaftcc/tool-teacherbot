---
title: CSC 114 Pilot Cohort — Corpus-Aware Cohort Spike
date: 2026-05-22
status: approved
---

# CSC 114 Pilot Cohort Design

## Why this exists

Teacherbot's System 1 is live on Render and currently serves five hardcoded
capstone groups. A separate course — CSC 114 (Fundamentals of Artificial
Intelligence and Machine Learning) — wants to pilot the tool next week with
two instructors and twelve students. The pilot needs:

1. A login the cohort can use (`csc114` / `2026su`).
2. The agent's responses to be informed by the course's specific corpus,
   which lives in an external repo
   (`https://github.com/norrisaftcc/course-csc114-template`,
   subfolder `planning/pilot_su26/`).
3. An update workflow that fits the project's "issue → branch → PR → merge"
   discipline so instructors can stage new weekly content without surprise.

This is a **spike**: the smallest credible solution that lets the cohort use
the system and gives us real feedback. Decisions favor "ship and learn" over
"design for every future course."

## Goal

By the end of the work described here, a member of the CSC 114 cohort can
visit the live URL, log in as `csc114` / `2026su`, and chat with an agent
whose system prompt contains the pilot's crosswalk plus week-01 and week-02
materials. Instructors can later add week-03 by editing one file and
opening a PR.

## Scope

### In scope

- Add `csc114` cohort credentials (replacing `group1`).
- Vendor the CSC 114 corpus into the repo under
  `system1-flask-chat/context/csc114/`.
- A sync script + manifest that pulls listed paths from the upstream repo,
  reproducibly, into the vendored directory.
- Extend `auth.load_group_context()` so that when a `csc114/` subdirectory
  exists, its files are concatenated into the context string returned at
  login.
- Unit-test the new concatenation behavior against fixtures.

### Out of scope (intentionally)

- Tool use / on-demand retrieval — corpus is concatenated whole into the
  system prompt.
- Per-cohort system prompts — the existing AlgoCratic voice in
  `claude_handler.build_system_prompt()` is reused unchanged.
- Relabeling the login UI from "Group ID" to "Cohort" or "Course."
- Migrating or renaming historical `group1` rows in the database.
- Token-budget tuning beyond a size check at sync time.
- Automating the sync (cron / GitHub Action). The instructor runs the
  script locally and opens a PR; that *is* the workflow.

## Current state (2026-05-22)

- System 1 is live: <https://teacherbot-6yut.onrender.com/>
- `system1-flask-chat/auth.py` holds five hardcoded groups
  (`group1`…`group5`), each with a password and a clearance level.
- `system1-flask-chat/context/group{1..5}_context.md` exist as
  instructor-edited briefs. `group1_context.md` is still a placeholder.
- `auth.load_group_context(group_id)` reads exactly one file:
  `context/{group_id}_context.md`. It is the only place the agent's
  per-cohort context originates.
- `claude_handler.build_system_prompt(group_context)` takes the loaded
  string and wraps it in the AlgoCratic pedagogy block. No tool use.
- Pushes to `main` auto-deploy to Render in roughly one minute.

## Architecture

### File layout after this work

```
system1-flask-chat/
├── auth.py                          # csc114 credential added; loader extended
├── context/
│   ├── group2_context.md … group5_context.md   (unchanged)
│   ├── csc114_context.md            # short, instructor-edited cohort header
│   └── csc114/                      # vendored corpus, written by sync script
│       ├── crosswalk.md
│       ├── week-01/…
│       └── week-02/…
└── tests/
    └── test_auth_context.py         # extended with concatenation cases

scripts/
├── sync_csc114_corpus.py            # idempotent sync from upstream
└── csc114_manifest.yaml             # paths + upstream ref
```

### Credentials

`auth.GROUPS` gains an entry and `group1` is removed:

```python
GROUPS = {
    'csc114': {'password': '2026su',    'clearance': 'ORANGE'},
    'group2': {'password': 'dataman2026', 'clearance': 'YELLOW'},
    'group3': {'password': 'finaid2026',  'clearance': 'ORANGE'},
    'group4': {'password': 'health2026',  'clearance': 'YELLOW'},
    'group5': {'password': 'sched2026',   'clearance': 'ORANGE'},
}
```

Clearance stays `ORANGE` so the existing system prompt's clearance-aware
behavior (if any future addition depends on it) keeps working unchanged.
Historical `Group` rows named `group1` in the production database are left
in place; a fresh `Group(name='csc114')` row is created on first login by
the existing `routes.login` flow.

### Context loading

`auth.load_group_context(group_id)` is extended:

1. Read `context/{group_id}_context.md` as today. Required.
2. If `context/{group_id}/` is a directory, walk it in sorted relative-path
   order and append the contents of every `.md` file beneath it, each
   prefixed with a header naming the relative path:

   ```
   {group_id}_context.md contents go here

   === CSC 114 CORPUS ===

   ## crosswalk.md
   <file contents>

   ## week-01/<filename>.md
   <file contents>
   ```
3. Non-`.md` files in the subdirectory are ignored with a logged warning.
   This keeps images, notebooks, etc. from being silently swallowed into
   the prompt.

The function signature does not change; callers continue to pass the
result to `claude_handler.build_system_prompt()`.

Concatenation happens once per login. The result is stored in
`session['group_context']` exactly as today, so per-message cost is paid
in the form of larger system-prompt tokens on each Anthropic call.

### Sync script

`scripts/csc114_manifest.yaml`:

```yaml
upstream: https://github.com/norrisaftcc/course-csc114-template
ref: main
target: system1-flask-chat/context/csc114
paths:
  - planning/pilot_su26/crosswalk.md
  - planning/pilot_su26/week-01/
  - planning/pilot_su26/week-02/
```

`scripts/sync_csc114_corpus.py` behavior:

1. Reads the manifest.
2. `git clone --depth 1 --branch <ref>` of `upstream` into a temp dir.
3. For each listed path: copies it into `target/`, flattening
   `planning/pilot_su26/` out of the destination tree so files land at
   `context/csc114/crosswalk.md`, `context/csc114/week-01/…` rather than
   the full upstream path.
4. Removes anything under `target/` that is *not* present after the copy,
   so deletions upstream propagate.
5. Prints a summary: file count, total bytes, approximate token count
   (rough heuristic: `bytes // 4`), and a warning if the estimate exceeds
   30k tokens.
6. Does **not** commit. The instructor reviews `git status`, stages, and
   commits manually.

The script is intended to be re-runnable; running it twice with no
upstream change yields no diff.

### Update workflow (the loop instructors actually use)

1. Open issue: `Sync CSC 114 corpus — week-03`.
2. Branch: `system1/csc114-sync-week03`.
3. Edit `scripts/csc114_manifest.yaml` to add the new week path.
4. Run `python scripts/sync_csc114_corpus.py` locally.
5. Inspect `git status` / `git diff` — the new content is right there.
6. Commit, push, open PR referencing the issue, get review, merge.
7. Render auto-deploy picks it up in roughly one minute.

This loop is the security model: nothing reaches students that didn't go
through a human-reviewed PR.

## Error handling

- **Sync script — upstream clone fails:** abort with a clear error. Don't
  touch `target/`.
- **Sync script — manifest references a path that doesn't exist upstream:**
  abort and report the missing path. Don't partially apply.
- **Sync script — corpus exceeds the size warning threshold:** print a
  prominent warning but still write the files. The instructor decides
  whether to ship.
- **Context loader — `csc114/` directory missing entirely:** behave
  exactly as before (return only `csc114_context.md`). This is the
  expected state in the first PR, before the sync script has been run.
- **Context loader — `csc114_context.md` missing:** raise
  `FileNotFoundError` with the existing instructor-facing message. The
  subdirectory alone is not sufficient.
- **Login flow:** unchanged. Existing `FileNotFoundError` handling in
  `routes.login` already flashes a clear message.

## Testing

- Unit tests in `system1-flask-chat/tests/test_auth_context.py`:
  - `csc114_context.md` alone returns just its contents.
  - `csc114_context.md` + a populated `csc114/` directory returns the
    concatenation in sorted-path order with the expected headers.
  - Non-`.md` files under `csc114/` are skipped.
  - Missing `csc114_context.md` raises `FileNotFoundError` even if the
    subdirectory exists.
- A small fixtures tree under `tests/fixtures/context_csc114/` backs these
  tests; tests do not touch the real `context/` directory.
- The sync script gets a smoke test: with a fixture manifest pointing at a
  tiny local "upstream" tarball or git repo (set up in the test), running
  the script produces the expected files in a temp `target/`.
- Manual verification before pilot day:
  1. Run the sync script, confirm the diff looks right, merge PR.
  2. Log into the live site as `csc114` / `2026su`, send a message that
     references something only the corpus would know (e.g., "What does
     the crosswalk say about week 02?") and confirm the agent's response
     reflects corpus content.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Corpus pushes the system prompt past a comfortable token budget. | Sync script prints size; flag at 30k-token estimate. Instructor decides. |
| Instructor forgets to run the sync after editing the manifest. | Manifest-only PRs are inert by design; the symptom is "nothing changed in chat." Document this in the runbook addition. |
| Upstream rewrites history on `main`, breaking reproducibility. | Manifest's `ref:` field accepts a pinned commit SHA. For the spike we use `main`; if reproducibility becomes an issue, pin. |
| Old `group1` password (`capstone2026`) is in instructor memory or notes. | Removal of `group1` from `GROUPS` makes it immediately non-functional; communicate the change to instructors before pilot day. |
| AlgoCratic voice lands oddly with CSC 114 students. | Accepted risk for the spike (chosen during brainstorming). Post-pilot review will revisit. |

## Implementation order

Three PRs, strictly in order. Each depends on the previous.

1. **PR A — `Add csc114 cohort credentials and context skeleton`**
   - `auth.py`: add `csc114`, remove `group1`.
   - `context/csc114_context.md`: instructor-editable cohort header
     (placeholder content acceptable for the spike).
   - `context/csc114/.gitkeep` so the directory exists.
   - Smallest deployable unit: login works, agent has just the header.

2. **PR B — `Add corpus sync script and manifest`**
   - `scripts/sync_csc114_corpus.py`, `scripts/csc114_manifest.yaml`.
   - First real sync committed in the *same* PR so reviewers see actual
     content land alongside the tooling.

3. **PR C — `Extend load_group_context to concatenate corpus directory`**
   - Loader change, fixtures, unit tests.
   - With PR A and PR B already merged, this is the change that flips the
     spike "on."

Each PR references its tracking issue and follows the standard
`system1/<topic>` branch naming.
