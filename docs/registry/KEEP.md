# KEEP — decision register

What this project has settled, what it is still negotiating, and what it owes.

Form borrowed from `norrisaftcc/the_algorithm`'s register. Two rules make it
worth keeping:

- **Every entry carries evidence.** A `file:line`, a test name, a measurement,
  or an ADR. An entry with no citation is an opinion and does not belong here.
- **Frozen means frozen.** A frozen entry is not reopened by argument, only by
  a new ADR that supersedes it. Negotiating entries are the live surface.

Why this file exists: `system1-flask-chat/DEPLOY.md` has instructed *"File
issues to track them before any production use"* for four named defects since
May. None were filed. The service ran live for two months and accumulated three
more that nobody had written down. This project's failure mode is not slow
coding — it is decisions that never get recorded, and so get re-litigated or
silently lost. Issue #2 deferred *"replacing query-string admin auth; adding
CSRF tokens"*; both are still true, neither was tracked anywhere, because the
deferral died with the issue.

---

## Frozen

### K1 — Only the corpus index and one active module reach the prompt

The full csc134 corpus is ~424 KB (~106k tokens). Loading it per message is what
the window exists to prevent.

*Evidence:* ADR-0002 and its amendment; `system1-flask-chat/auth.py:226-286`;
`auth.py:77-89` (`module_window`).

### K2 — Instructor-facing files are never vendored

A course repo keeps answer keys next to the readings they answer. Anything
vendored can reach the system prompt, where no persona wording reliably holds it
back. Patterns target files that say so about themselves: `*-key.md`
(`audience: instructor`), `*.STUB.md`, `_assets.md`.

*Evidence:* `scripts/csc134_manifest.yaml` exclude block;
`scripts/sync_course_corpus.py:41-49`.

### K3 — Eval flags are triage, never a verdict

The harness catches failures with a *shape*. It cannot catch a confident false
statement about the subject matter, and a checker that could is another model
that can also be wrong. Flags narrow the reading; a human still reads the
transcript.

*Evidence:* `scripts/eval_persona.py:154-163`.

Worth noting: this is teacherbot independently arriving at ASSAY's stance —
*this is a finding, not a draft*. ADR-0005 §8 is the first case where the rule
can be relaxed, and only because a byte-exact fixed string is not an
approximation.

### K4 — First-years never see a pull request

Confirmed by the course lead: CSC 134 students submit with stage/commit/push and
are not put in front of a PR at all. The fork/branch/PR walkthrough relocates to
the M8 capstone.

*Evidence:* `system1-flask-chat/context/csc134_persona.md`; eval item `m0-03`;
`scripts/csc134_manifest.yaml` excludes `assignments/m0/02_first_pull_request.md`.

### K5 — A local model result is not a pass

Only the Anthropic run decides anything. The Ollama backend narrows the search
for free. Demonstrated rather than asserted: on `m0-07`, `llama3.2:3b` was wrong
twice with the same notes in the prompt that Haiku got right — the item measures
model capability, not prompt content.

*Evidence:* ADR-0003; `evals/csc134/m0.yaml`; commit `740305c`.

### K6 — No schema change to an existing table until Alembic lands

> **Superseded by ADR-0006 (2026-07-29).** Alembic landed. Kept in full because
> ADR-0004 was designed around this constraint and reads oddly without it, and
> because the register's rule is that frozen entries are superseded, not edited.

`db.create_all()` creates missing tables and does nothing else. A new table is
free on the next deploy. A new column on an existing table silently does nothing
and then raises `UndefinedColumn` in production — on a service that auto-deploys
from `main`. Tests cannot catch it: they run on in-memory SQLite, which builds
the schema fresh every run.

*Evidence:* `system1-flask-chat/app.py` (`db.create_all()` at startup);
`system1-flask-chat/requirements.txt` (no Alembic, no Flask-Migrate);
`system1-flask-chat/tests/conftest.py:7`.

*What changed:* Flask-Migrate is now a runtime dependency, `create_all()` is
gated on `TESTING`, and `tests/test_migrations.py` fails CI when a model and the
migrations disagree. The prohibition existed because nothing could *detect* the
mistake; that detector now exists. See K14 and K15.

### K7 — Secrets have no fallbacks

`SECRET_KEY` and `ADMIN_PASSWORD` used to fall back to `dev-secret` and `admin`.
Both are `sync: false` in `render.yaml`, so an operator sets them by hand and can
forget — and forgetting was silent: the service came up healthy while signing
session cookies with a value published in this public repo. `create_app` now
refuses to start.

*Evidence:* `system1-flask-chat/app.py` (`_require_secrets`);
`system1-flask-chat/tests/test_app.py`.

### K14 — Alembic owns the production schema; `create_all` is for tests only

They must never both run against a real database. `create_all()` writes no
`alembic_version` row, so a table it builds is invisible to Alembic, and the next
migration fails on a table that already exists. Migrations are applied by
`preDeployCommand: flask db upgrade`, never by the app at boot.

*Evidence:* `system1-flask-chat/app.py` (the `TESTING` gate);
`system1-flask-chat/tests/test_migrations.py`; ADR-0006 §2, §3.

### K15 — A migration is rehearsed on staging before it reaches `main`

The suite runs on SQLite, which accepts things Postgres rejects — type changes,
constraints added against existing data, a non-null column on a populated table.
`test_migrations.py` proves a migration matches the models; only a Postgres run
proves it survives real data. `teacherbot-db-staging` exists for exactly this and
is not a general-purpose production clone.

*Evidence:* ADR-0006 §5; `render.yaml`.

### K16 — Live tests gate on mechanics, never on persona judgement

`ANTHROPIC_API_KEY` is a repo secret, so tests can hit the real API. What
they may *gate* on is bounded by K3: caching engaging, the composed prompt
being accepted, `_usage_total` matching the SDK — all facts. Whether the bot
answered well stays a report.

The temptation is obvious and should be named: a green checkmark for "the
bot behaved" is exactly what a course lead wants and exactly what the eval
harness cannot honestly provide. `eval_persona.main()` returns 0 whether or
not items are flagged, so a job wired to gate on it would be a gate in
appearance only — worse than no gate, because it would be trusted.

If that changes, it changes via an ADR that supersedes K3, and the thing
that would justify it is `--runs N` with a rate (#30) plus a byte-exact
pass condition (ADR-0005 §8) — not a single sample of a judgement call.

*Evidence:* `.github/workflows/live.yml`;
`system1-flask-chat/tests/test_live_anthropic.py`; `pytest.ini` (`-m "not live"`).

### K18 — Code the course hands over is quotable; code the student is graded on writing is not

The line "never hand over a solution" has no meaning until you say which code is
whose. The corpus hands students code constantly — setup snippets, walkthrough
steps, the `int main() { // Your code here  return 0; }` skeleton every M1
assignment prints under *"Your code structure should follow this pattern"*.
Quoting that is pointing at the material, which is the job. The body of the
program — the output lines, the logic, the calculation — is the deliverable and
is not the bot's to write.

Getting this wrong is not hypothetical: eval item `m0-02` demanded a refusal of
the exact code `assignments/m0/01_workspace_setup.md` Step 4 tells the student to
paste. Five live samples were spent before anyone noticed the item was ill-posed
rather than the model unstable. The item was retired, not repaired, and its id
was not reused so the `observed_variance` history still reads.

The refusal also has a shape rather than being a wall: *go through the gate
together and write the pseudocode first.* A student out of time leaves with a
plan they wrote and can defend. This is the gate as a helping posture, held by
the bot — **not** the gate curriculum, which K13 keeps away from first-years, and
not student-held gate authority, which `the_algorithm`'s K17 scopes to late
capstone.

Numbered K18, skipping K17, because this repo cites `the_algorithm`'s K17 by name
often enough that a local K17 would read as the same entry.

*Evidence:* `system1-flask-chat/context/csc134_persona.md`
(*"WHAT COUNTS AS 'THE SOLUTION'"*, rule 1); `scripts/eval_persona.py`
(`_handed_over_a_solution`); `tests/test_eval_persona.py`
(`test_does_not_flag_the_skeleton_the_corpus_hands_over`); `evals/csc134/m1.yaml`
item `m1-03`, which fails if the bot *withholds* the skeleton.

---

## Negotiating

### K8 — What survives a session boundary

Position taken in ADR-0004 §3: a frozen artifact survives, an open negotiation
does not. Decides the `Exchange.frozen_at` column, so it cannot be deferred past
the schema.

*Status:* ADR-0004, Proposed. Tracked in #20.

### K9 — Student identity under a shared cohort passcode

Position taken in ADR-0004 §1: cohort passcode plus a declared GitHub handle,
explicitly unverified, adequate only because the instructor holds corroborating
commit authorship and a capstone cohort is small.

*Status:* ADR-0004, Proposed. Tracked in #20.

### K10 — The budget's unit, owner, and denomination

Three open questions in one. The **owner** should move from cohort to seat
(ADR-0004 §2) so one verbose student cannot lock out the class. The
**denomination** is undecided: `_usage_total` counts cache reads at full weight,
which is a correct token count and a poor cost proxy — cache reads bill at
roughly a tenth of list, 1h cache writes at roughly double. Picking one needs a
measurement, not an inherited constant.

*Evidence:* `system1-flask-chat/claude_handler.py:54-66`;
`system1-flask-chat/models.py` (`DEFAULT_TOKEN_BUDGET`, `raise_budget_floor`).
*Status:* partially addressed — the number was resized as a stopgap; the unit is
still wrong. Tracked in #20.

### K11 — What the repointed csc114 slot becomes

Position taken in ADR-0005: the slot becomes the Prompt Wizard under the slug
`algorithm`, on Sonnet, with the doctrine always-on rather than windowed.

*Status:* ADR-0005, Proposed. Tracked in #21.

### K12 — Retention of the CSC 114 pilot rows

> **Closed, moot (2026-07-29).** The course lead ruled the old free-tier
> resources written off. That database was provisioned around 2026-05-17 against
> a 30-day expiry, so it had most likely lapsed already; it held demo traffic and
> a finished pilot. There is nothing left to export, so this no longer blocks the
> ADR-0005 repoint.

Once no skin serves `csc114`, `/csc114/admin` stops existing and the pilot's
transcripts are unreachable — the `Group` row stays in Postgres with no route to
it.

*Status:* closed. #22 closed as not-planned.
`scripts/export_group_transcripts.py` stays — the next cohort to be retired will
want it, and it now has a rehearsed path.

### K13 — Whether teacherbot teaches The Algorithm, and to whom

Position taken in ADR-0005: yes, at `/algorithm`, and **not** to CSC 134.
`the_algorithm`'s K17 scopes gate authority to late capstone; week-1 first-years
are the far end of the linear-implementor side, so teaching them to hold a gate
implements the opposite of what that register says.

*Status:* ADR-0005, Proposed. Tracked in #21. Recorded here so it stops being
reopened.

---

## Backlog

Each row carries its evidence and links to its issue. B11-B13 share one thread.

| # | Item | Evidence |
|---|---|---|
| ~~[B1](https://github.com/norrisaftcc/tool-teacherbot/issues/23)~~ | ~~**Alembic / Flask-Migrate**~~ — **done**, ADR-0006. Landed before the capstone rather than after, and on a fresh database so the baseline needed no hand-run `stamp`. | ADR-0006 |
| [B2](https://github.com/norrisaftcc/tool-teacherbot/issues/24) | **SHA-pin the corpus sync.** `fetch_upstream` uses `git clone --branch`, which cannot take a SHA, so every manifest tracks a moving branch and no provenance SHA is recorded. Prerequisite for ADR-0005. | `scripts/sync_course_corpus.py:33-38` |
| ~~[B3](https://github.com/norrisaftcc/tool-teacherbot/issues/25)~~ | ~~**Pin `marked` and add SRI**, or vendor it into `static/js/`.~~ — **done** in #41, which vendored `marked@18.0.7` and dropped the CDN tag; #42 then repointed the XSS check at the vendored bytes rather than the npm build. The row outlived its fix and was caught by a gap analysis rather than by anyone reading the register — the same drift this file exists to prevent, one level up. | `static/js/marked.umd.js`; `system1-flask-chat/tests/js/render_check.mjs` |
| [B4](https://github.com/norrisaftcc/tool-teacherbot/issues/26) | **Admin auth is a URL query parameter.** `?password=…` lands in Render access logs and browser history. Replace with a POST form. Deferred by issue #2 and never tracked. | `system1-flask-chat/routes.py:271` |
| [B5](https://github.com/norrisaftcc/tool-teacherbot/issues/27) | **No CSRF protection.** `flask-wtf` is not in requirements. Deferred by issue #2 and never tracked. | `system1-flask-chat/requirements.txt` |
| [B6](https://github.com/norrisaftcc/tool-teacherbot/issues/28) | **`increment_tokens` has a read-modify-write race.** Two concurrent requests can both read the old value. Harmless at a cohort's message rate; not harmless as a graded ledger. | `system1-flask-chat/models.py:48` |
| [B7](https://github.com/norrisaftcc/tool-teacherbot/issues/29) | **Admin view is read-only.** No budget editing, no transcript reading — conversations are fetched and never rendered. | `system1-flask-chat/routes.py:269`; `templates/admin.html` |
| ~~[B8](https://github.com/norrisaftcc/tool-teacherbot/issues/30)~~ | ~~**`--runs N` for the eval harness.**~~ — **done** in #44. `live.yml` samples each item three times, the smallest N that distinguishes always / never / sometimes. An item that is clean twice and flagged once now prints `VARY` rather than being rounded to either neighbour. Still not a gate: K16 wants a rate *and* a byte-exact pass condition, and this is the first half. | `scripts/eval_persona.py` (`verdict`); `.github/workflows/live.yml` |
| [B9](https://github.com/norrisaftcc/tool-teacherbot/issues/31) | **Test deps ship to production.** `pytest` and `pytest-flask` are in the requirements file Render installs. | `system1-flask-chat/requirements.txt` |
| [B10](https://github.com/norrisaftcc/tool-teacherbot/issues/32) | **Stale root documentation.** ~3,269 lines across nine files describe a five-group project shape that no longer exists; `README.md` still advertises deleted credentials. | `README.md`, `CLAUDE.md`, and seven others |
| [B11](https://github.com/norrisaftcc/tool-teacherbot/issues/33) | **`.DS_Store` is tracked** at the root and in `design/`. `.gitignore` covers only the latter, which is inert since it is already tracked. | `.gitignore:219` |
| [B12](https://github.com/norrisaftcc/tool-teacherbot/issues/33) | **Flask-Login is vestigial.** Initialised, `load_user` returns `None`, auth is entirely session-based. Either use it or drop the dependency. | `system1-flask-chat/app.py` |
| [B13](https://github.com/norrisaftcc/tool-teacherbot/issues/33) | **`design/system1/*.jsx` are not wired into the app** and reference a `terminal.css` that no longer exists. | `docs/design/design-guidelines.md` |
