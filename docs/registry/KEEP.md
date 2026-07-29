# KEEP — decision register

What this project has settled, what it is still negotiating, and what it owes.

Form borrowed from `norrisaftcc/the_algorithm`'s register. Three rules make it
worth keeping:

- **Every entry carries evidence.** A `file:line`, a test name, a measurement,
  or an ADR. An entry with no citation is an opinion and does not belong here.
- **Frozen means frozen.** A frozen entry is not reopened by argument, only by
  a new ADR that supersedes it. Negotiating entries are the live surface.
- **Every frozen entry carries a `Rejected:` line.** It names the options that
  lost and the cost that ruled each out. An entry that froze without an
  alternative says so instead — *"Rejected: nothing; no alternative was raised."*

The third rule exists because freezing is destructive. A `## Negotiating` entry is
rewritten in place when it freezes, and the argument evaporates with it — the
register keeps the answer and loses the reasoning, which is the half you need when
the same question returns in six months wearing different clothes. `Rejected:` is
the compressed negotiation, always present. The full negotiation is always
recoverable: `git log -p docs/registry/KEEP.md`. No index, no second file, no
maintenance — the history is a property of the repo, not a thing to curate.

**The rule is prospective, and the file does not yet satisfy it.** Eleven frozen
entries predate it — K1-K7, K10, K14, K15, K16 — and are not being backfilled in
the same change that introduces the rule. Writing eleven `Rejected:` lines now
would mean reconstructing arguments from recollection rather than from the ADRs
that recorded them, which is the failure #48 spent a whole PR correcting. Tracked
as B15 against the ADRs where the reasoning is actually recoverable; entries frozen
after 2026-07-29 carry the line from the start.

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

### K8 — A frozen artifact survives a session boundary; an open negotiation does not

Frozen 2026-07-29 by the course lead, having been the live surface since
2026-07-28. Decides `Exchange.frozen_at`.

The memory is asymmetric. `frozen_at NOT NULL` is replayed **byte-exact** into
the system prompt — it is a contract, and quoting a contract claims no new
authority. `frozen_at IS NULL` is shown to the student as history and is **never**
re-entered as an operative floor.

The asymmetry is the safety property, not an optimisation. Open negotiation
state is the machine's inference about what the human *seems* to want, and
replaying it across a boundary re-asserts inferences nobody ratified — against a
student whose recollection has decayed over a week while the database's has not.
That is manufactured consent. This repo already names the shape one layer down:
`m0-04`, failure mode `invented-a-date` — *"The worst outcome in the bank. A
confident wrong date is acted on."* A confidently restated unfrozen floor is an
invented date about the student's own intent.

Rejected: **replay everything** — simpler, and what "add memory" usually means;
produces a turn log rather than a record of freeze events. **Replay nothing** —
safe and close to what already exists, so it does not deliver the stated want.

*Evidence:* ADR-0004 §3, §4 (Accepted). Tracked in #20.

### K9 — Identity is a declared GitHub handle, and it is unverified

Frozen 2026-07-29. Login keeps the shared cohort passcode and adds one field: the
student's GitHub username. That handle keys their memory and their transcripts.

**Unverified, and this says so rather than implying otherwise** — a student can
type a peer's handle. Adequate for the capstone for two reasons that will not
hold forever: the instructor holds corroborating commit authorship from
Codespaces, which is what makes a self-declared handle usable for a graded
artifact; and a capstone cohort is small enough that impersonation is a social
problem. GitHub OAuth is the upgrade, and it is an upgrade rather than a rewrite
because it fills the same column.

Rejected: **OAuth now** — right eventually, but it blocks the schema behind an
integration the capstone does not have time for. **Opaque seat tokens** —
anonymous, die with the cookie, produce nothing gradeable.

*Evidence:* ADR-0004 §1 (Accepted). Tracked in #20.

### K10 — The budget belongs to the seat and is denominated in tokens as counted today

Frozen 2026-07-29. Both halves, where previously only the owner had a position.

**Owner: the seat.** Per-cohort pooling means one verbose student can exhaust the
class, which is a defect today and worse once replay raises per-message spend
against the same pool.

**Denomination: tokens, as `_usage_total` already counts them** — cache reads at
full weight. This is a correct token count and a poor cost proxy, and it is now
*deliberately* that rather than pending a decision. Weighting the counters toward
real billing (cache reads ~0.1, 1h writes ~2) was the alternative and was
declined: it trades an honest count for an estimate resting on hardcoded pricing
ratios that would go stale silently. If a cost figure is ever needed, it is a
reporting concern, not the budget's unit.

*Evidence:* ADR-0004 §2 and §"Consequences" (Accepted);
`system1-flask-chat/claude_handler.py:63-75` — the comment there is a
description, not an open question. Tracked in #20.

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
proves it survives real data. `teacherbot-pro-db-staging` exists for exactly this
and
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

*Rejected:* **"never hand over code"** — the rule as previously written, which the
corpus violates on nearly every assignment page. **Enumerating quotable files** —
precise, and stale the first time the corpus syncs.

### K19 — The repo never mandates a skill it does not install

A document may record that an agent workflow was used. It may not instruct its
reader to adopt one.

Skills and plugins are resolved per session, from the environment. A document that
requires one is a dependency with no manifest and no failure mode: when the skill
is absent, nothing errors — the agent either stalls or improvises, and the
document cannot tell which happened. This is worse than an unpinned version,
because there is no lockfile to inspect and no name to grep for in a dependency
list.

The compounding case is a **superseded** document that opens with an imperative.
Four planning docs began with *"REQUIRED SUB-SKILL: Use superpowers:…to implement
this plan task-by-task"*, naming skills that no session in this repo has ever had
installed. Three of them had been given a *"do not act on this document"* banner
in #48 — with the mandate left intact two lines below it. First line wins over
fourth: the imperative gets acted on before the banner is read. Marking a document
stale and leaving its instruction voice intact is not marking it stale.

The directives were struck and replaced with a descriptive line, and both
`docs/superpowers/` and `docs/plans/` were folded into `docs/historical/` —
`superpowers/` named a vendor's workflow as though it were this project's
structure, and that framing is what made the mandate look like it belonged.

*Rejected:* **downgrade "REQUIRED" to "recommended"** — keeps a
dependency-with-no-manifest, just quieter. **Delete the documents** — they hold
the reasoning behind the Render bootstrap that `DEPLOY.md` still points at as its
fallback procedure. **Banner only, leave the imperative** — what #48 did, and the
contradiction is the defect.

*Evidence:* four `REQUIRED SUB-SKILL` directives naming `superpowers:*`, none
installed in the session that found them (`/root/.claude/plugins/` empty, absent
from the skill list). Struck in this change; `grep -rn "REQUIRED SUB-SKILL" .`
returns nothing.

---

## Negotiating

> **K8, K9 and K10 moved to Frozen on 2026-07-29**, answered by the course lead
> and recorded in ADR-0004, which moved to Accepted in the same change. They were
> the last three questions blocking the memory schema.

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
| [B7](https://github.com/norrisaftcc/tool-teacherbot/issues/29) | **Admin view is read-only.** No budget editing, and no *full* transcript reading. **Corrected 2026-07-29:** this row said conversations "are fetched and never rendered" — `admin.html:68-101` does render them (group, `started_at`, message count, last user message previewed to 80 chars). What is missing is the full transcript, which is a smaller gap than the row claimed and a larger rework, since the template traverses relationships off the tables ADR-0004 drops. No test covers the render branch: the one admin test runs with no `Group` row, so the loop never executes. | `system1-flask-chat/routes.py:310-326`; `templates/admin.html:68-101` |
| ~~[B8](https://github.com/norrisaftcc/tool-teacherbot/issues/30)~~ | ~~**`--runs N` for the eval harness.**~~ — **done** in #44. `live.yml` samples each item three times, the smallest N that distinguishes always / never / sometimes. An item that is clean twice and flagged once now prints `VARY` rather than being rounded to either neighbour. Still not a gate: K16 wants a rate *and* a byte-exact pass condition, and this is the first half. | `scripts/eval_persona.py` (`verdict`); `.github/workflows/live.yml` |
| [B9](https://github.com/norrisaftcc/tool-teacherbot/issues/31) | **Test deps ship to production.** `pytest` and `pytest-flask` are in the requirements file Render installs. | `system1-flask-chat/requirements.txt` |
| [B10](https://github.com/norrisaftcc/tool-teacherbot/issues/32) | **Stale root documentation.** ~3,269 lines across nine files describe a five-group project shape that no longer exists; `README.md` still advertises deleted credentials. | `README.md`, `CLAUDE.md`, and seven others |
| [B11](https://github.com/norrisaftcc/tool-teacherbot/issues/33) | **`.DS_Store` is tracked** at the root and in `design/`. `.gitignore` covers only the latter, which is inert since it is already tracked. | `.gitignore:219` |
| [B12](https://github.com/norrisaftcc/tool-teacherbot/issues/33) | **Flask-Login is vestigial.** Initialised, `load_user` returns `None`, auth is entirely session-based. Either use it or drop the dependency. | `system1-flask-chat/app.py` |
| [B13](https://github.com/norrisaftcc/tool-teacherbot/issues/33) | **`design/system1/*.jsx` are not wired into the app** and reference a `terminal.css` that no longer exists. | `docs/design/design-guidelines.md` |
| B14 | **Moving a session between a local workstation and the cloud, when only one of the two can reach the deploy target.** Tabled explicitly by the course lead. This session is the first concrete instance: planning ran in a cloud container that cannot reach `api.render.com` (403 at the egress proxy) or port 5432, so every Render action had to be authored here and executed elsewhere. There is no mechanism for handing partial state across that boundary — the plan file and the git branch are doing it by hand. Recorded so it is not re-discovered a third time. | this session; `curl https://api.render.com/v1/services` → `CONNECT tunnel failed, response 403` |
| B15 | **Backfill `Rejected:` lines on the eleven frozen entries that predate the rule** — K1-K7, K10, K14, K15, K16. Recover the alternatives from the ADRs that recorded them, not from recollection. An entry whose ADR names no alternative gets *"Rejected: nothing; no alternative was raised"* rather than an invented one. | `docs/registry/KEEP.md` header rule 3; `docs/adr/` |
