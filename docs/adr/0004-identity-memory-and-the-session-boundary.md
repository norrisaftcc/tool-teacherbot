# ADR-0004: Seat identity, server-side memory, and the session boundary

- **Status:** Accepted (2026-07-29). Proposed 2026-07-28.
- **Deciders:** norrisaftcc (product), Claude Code (implementation)

**Amended before acceptance.** ADR-0006 landed Alembic the day after this was
written, which falsified the constraint §"The constraint that forces this
decision now" was built on. The three open questions (K8, K9, K10) were then put
to the course lead and answered; §2 changed as a result. The amendments are
marked inline rather than folded in silently, because the reasoning that was
wrong is the useful part of the record.

| Question | Frozen answer |
|---|---|
| Schema shape | New tables **and drop the legacy two** — see §2 |
| K9 · identity | Declared GitHub handle, explicitly unverified — §1, unchanged |
| K10 · budget | Per-seat, denominated in tokens as counted today — §2, §"Consequences" |
| K8 · session boundary | Asymmetric: frozen replays, open does not — §3, unchanged |

### Second amendment, 2026-07-29 — scope, after a readiness review

A four-agent review of this record against the code found three factual errors
in it (marked inline below as corrections) and two design gaps neither this ADR
nor the register owned. The course lead answered four further questions. **The
effect is to narrow what ships, not to change what was frozen.**

| Question | Answer | Consequence |
|---|---|---|
| What does a frozen exchange replay? | **Nothing yet.** `frozen_at` ships as a nullable column that no endpoint writes and no code reads. | §3's asymmetry is *specified* but not *implemented*. The replay branch does not exist, so it cannot ship as unreachable dead code, and the escalation risk below cannot fire. |
| What bounds turn replay? | **The last N turns, N fixed and small.** | See §5. Without it, cumulative spend is quadratic in turn count. |
| What is the per-seat budget? | **Measure first.** The cohort ceiling stays as a backstop; the seat number is set from a measurement once replay is live. | K10's own text asks for "a measurement, not an inherited constant"; the old 25M÷seats arithmetic assumed constant per-message cost, which memory breaks. |
| Spike or build? | **Spike first**, on staging, throwaway. | Also settles what exists on Render, which is the real first blocker. |

**§4 named a column that does not exist.** It says the assessable unit is
"`frozen_at` plus the floor's content at freeze time" — and the DDL has only the
timestamp. Deferring the freeze semantics is what resolves that: the floor's
storage is decided in the follow-on ADR that implements it, alongside the
mitigation below.

**A gap this record did not own: K8 × K9 compose into a write primitive.**
K9 makes the handle client-supplied, unverified and free to mint, and it *keys
the seat*. K8 says frozen content is replayed "byte-exact" into the **system
prompt**. So a student could log in with the shared cohort passcode, type a
peer's handle, freeze a floor, and have it replay above the persona's
pedagogical rules in that peer's next session. K9's justification is written
entirely against a *read* threat — impersonation, corroborating commit
authorship. Commit authorship attributes work; it says nothing about writing
into someone else's operative floor.

This does not reopen K8 or K9. §3 already requires that resuming a frozen
exchange emit a confirmation the human must answer — **that confirmation is the
mitigation**, and the follow-on ADR must say so explicitly rather than leaving
it as a UX detail. Deferring the freeze means nothing is exposed meanwhile.

## Context

The stated direction is memory: students should be able to talk to the
interface without reinventing the wheel every time. The capstone this system
was built for is weeks off, and it is the first cohort that will be *assessed*
on how it works with an agent.

Three facts about what exists today, all verified against the code.

**1. There is no memory. There is a page variable.**

`static/js/chat.js:70` is `let history = []`. The browser holds it, the browser
sends it (`chat.js:89`), and `routes.py:189` and `routes.py:241` read it back
off the request body. Refresh the tab and the conversation is gone. That is the
whole of it.

**2. The database is write-only.**

Both chat paths create `Message` rows (`routes.py:174-177`, `routes.py:242-245`).
Nothing reads them back into a prompt — `Message.query` appears nowhere in the
codebase. `Conversation` and `Message` are a log for the admin view, not a
memory.

**3. There is no student. There is a cohort.**

`routes.py:118` creates exactly one `Group` row per skin slug. So the
conversation lookup at `routes.py:166-169`, repeated at `routes.py:232-237`:

```python
conv = (Conversation.query
        .filter_by(group_id=group.id)
        .order_by(Conversation.started_at.desc())
        .first())
```

selects the most recently started conversation *in the entire cohort*. Two
students chatting at once interleave into one row. The `if not conv or not
history:` branch at `routes.py:170` and `:238` compounds it: a client sending
empty history forks a new conversation, a client sending non-empty history
appends to whatever the cohort last touched. The transcript is neither
attributable nor coherent.

And because history is supplied by the client, it is forgeable. A student can
POST a fabricated prior assistant turn establishing that full solutions are
fine in this conversation. For a bot whose first pedagogical rule is refusing
to hand over solutions, that is a live weakness, not a theoretical one — it is
a `fetch` in devtools.

### Why this blocks more than convenience

`the_algorithm`'s decision register (K17) holds that the assessment artifact
for the gate curriculum already exists in *frozen negotiation transcripts*, and
distinguishes instructor-held gate authority in early capstone from
student-held gate authority in late capstone, where holding the gate is the
graded skill. Teacherbot is the runtime that would produce those transcripts.

A transcript that lives in a page variable, mixes three students together, and
can be edited by the person being graded is not an assessment artifact. So
identity is a precondition for memory, and memory is a precondition for the
gradebook.

### The constraint that forced this decision — since lifted

> **Superseded by ADR-0006 (2026-07-29), one day after this was written.**
> Alembic and Flask-Migrate landed, `create_all()` is gated on `TESTING`, and
> `tests/test_migrations.py` fails CI when models and migrations disagree. The
> argument below is no longer true and the design no longer rests on it.
>
> It is kept in full, and this ADR was not frozen until it was reread, because
> the difference matters: "new tables only" was a **forced move** when written
> and is a **choice** now. An unexamined constraint that outlives its cause is
> how a workaround becomes an architecture. On rereading, the shape survived on
> its own merits — `Turn` needs a `seq` that `Message` lacks, `Exchange` needs
> `frozen_at`, and neither is an ALTER anybody wants — but the *rejection* at
> "Alternatives Considered" no longer stands on impossibility, only on
> preference, and §2 changed as a direct result.

`app.py` runs `db.create_all()` on startup and there is no migrations framework
— no Alembic, no Flask-Migrate in `requirements.txt`. `create_all()` creates
*missing tables* and does nothing else.

- A **new table** appears on the next deploy. Free.
- A **column added to an existing table** silently does nothing on deploy, and
  every query naming it then raises `UndefinedColumn` — in production, on a
  service with `autoDeploy: true` from `main`.

Tests cannot catch that: `tests/conftest.py:7` uses `sqlite:///:memory:`, where
`create_all` builds the schema from scratch each run and the divergence is
invisible.

So the memory schema gets one cheap shot. Every question below decides a column,
and getting one wrong means an Alembic migration against live Postgres under
capstone time pressure. That is why this is an ADR and not a commit.

## Decision

### 1. Identity: cohort passcode, then a declared GitHub handle

Login keeps the shared cohort passcode and adds one field: the student's GitHub
username. That handle keys their memory and their transcripts.

**It is unverified, and this record says so plainly rather than implying
otherwise.** A student can type a peer's handle. This is acceptable for the
capstone, for two reasons that will not hold forever:

- The capstone runs on GitHub and students are already working in Codespaces,
  so the instructor holds corroborating commit authorship. The cross-check is
  what makes a self-declared handle adequate for a graded artifact — the handle
  alone is not.
- A capstone cohort is small enough that impersonation is a social problem
  rather than a technical one.

When the cohort is large enough that this stops being true, GitHub OAuth is the
upgrade. It is an upgrade and not a rewrite, because the handle column is the
same column.

Rejected: **opaque server-issued seat tokens** — anonymous, die with the cookie,
produce nothing gradeable. **Per-student passcodes** — real attribution, but N
credentials to administer per cohort, and passcodes currently live in a public
repo.

### 2. Three new tables, and the legacy two are dropped

> **Amended 2026-07-29.** Originally *"and no change to any existing one"* — a
> title that described the migration-less constraint above, not a preference.
> With Alembic in place the course lead ruled: add the three, and **drop
> `conversations` and `messages`** rather than leaving them as a dead log.

```
Seat      id, group_id FK, handle, created_at, last_seen_at,
          token_budget, tokens_used
          UNIQUE (group_id, handle)

Exchange  id, seat_id FK, started_at, ended_at,
          frozen_at   (nullable timestamp — see §3)
          mode        (nullable: 'provide' | 'assay')

Turn      id, exchange_id FK, seq, role, content, tokens_used, created_at
          UNIQUE (exchange_id, seq)
```

Alembic now applies all of this, so the shape is argued on merit rather than on
what `create_all()` can reach. `Turn` needs a `seq` that `Message` does not have
and an ordering guarantee it cannot give; `Exchange` needs `frozen_at`, which is
the entire point of §4. Retrofitting both onto `Conversation`/`Message` reaches
the same schema through several ALTERs against live Postgres, each owing a K15
staging rehearsal. Adding the tables is the smaller real diff even though it is
the larger apparent one.

**The budget moves to `Seat`,** denominated in **tokens as `_usage_total`
already counts them** — cache reads at full weight. That is a correct token
count and a poor cost proxy, and K10 now freezes it as *deliberately* a token
count rather than leaving the denomination open. The alternative was weighting
cache reads to ~0.1 and 1h writes to ~2, which buys a better spend estimate at
the price of hardcoded pricing ratios that go stale silently. Moving the budget
off `Group` also fixes a defect that exists today independently of memory: the
pool is per-cohort, so one verbose student can exhaust the class — and replay
raises per-message spend against that same shared pool.

**The legacy tables are dropped, not retained.** `conversations` and `messages`
hold demo traffic plus the finished CSC 114 pilot, which K12 already wrote off as
moot. This is the **first Alembic migration against production data and the first
destructive one**, so K15 binds hard: rehearse on `teacherbot-pro-db-staging`
first — and **seed it**, because `flask db upgrade` against an empty Postgres
proves the DDL parses and nothing else. See also the note below on whether there
are any production rows left to destroy.
`tests/test_migrations.py` runs on SQLite and will not tell you what Postgres
does with a DROP against live rows and live foreign keys.

Everything reading those tables moves in the same change or breaks. Verified
against the code, not assumed:

| Reader | Fate |
|---|---|
| `scripts/export_group_transcripts.py:57-66` | **The one that dies quietly.** K12 keeps this script for the next retired cohort and it reads *only* the legacy tables. Repoint it at `Seat`/`Exchange`/`Turn` or K12 becomes false. |
| `routes.py:210-220`, `:278-288` | Both chat write paths. They stop writing `Conversation`/`Message` and start writing `Turn`. |
| `routes.py:310-326` + `templates/admin.html:68-101` | The admin view (#29). **Correction (2026-07-29):** this record and KEEP B7 both said the conversations are "fetched and never rendered." They are rendered — group name, `started_at`, message count, and the last user message previewed to 80 chars. The template traverses `conv.group`, `conv.messages`, `m.content`, so the rework is larger than "start rendering what you already fetch", and no test catches a regression there: `test_admin_accessible_with_correct_password` hits admin with no Group row, so `conversations` is empty and the render branch never executes. |
| `models.py:80` | `Group.conversations` relationship. |
| `templates/chat.html:44` | Student-facing copy: *"Conversations logged for instructor review."* |

### 3. A frozen artifact survives a session boundary. An open negotiation does not.

This is the question that decides `frozen_at`, so it has to be settled before
the table exists.

The freezing verb is an act by a live human at a moment in time. Its *product*
— the frozen floor — is a record, and records persist. Replaying a frozen floor
into a resumed session is **quoting**, not re-freezing. No new authority is
claimed. This is also what makes the transcript gradeable at all: an artifact
that evaporates at the session boundary cannot be an assessment artifact.

Open negotiation state is a different kind of thing. It is not a record of what
the human ratified; it is the machine's working inference about what the human
*seems* to want. Replaying it across a boundary silently re-asserts inferences
that were never ratified, and the asymmetry is what makes it dangerous: across a
week the student's recollection of the session decays and the database's does
not. The agent resumes stating a floor with full confidence, the student does
not remember disagreeing, and consent is manufactured.

This repo already names that failure one layer down. `evals/csc134/m0.yaml`,
item `m0-04`, failure mode `invented-a-date`: *"The worst outcome in the bank. A
confident wrong date is acted on."* A confidently restated unfrozen floor is an
invented date about the student's own intent.

So the memory is asymmetric:

| State | On resume |
|---|---|
| `frozen_at NOT NULL` | Replayed verbatim into the system prompt. Byte-exact — it is a contract. |
| `frozen_at IS NULL` | Shown to the human as history. **Not** re-entered into the system prompt as an operative floor. |

Resuming a frozen exchange emits a fixed string that displays the frozen floor
and asks whether it still holds. That confirmation is itself a freezing verb, so
the gate stays human-opened and nothing is inherited silently.

### 4. The assessable unit is the freeze event, not the conversation

Server-side memory is necessary but not sufficient for the gradebook. What K17
wants graded is whether the student *held the gate correctly* — froze at the
right moment, with the right floor, having elicited the right gaps. A raw turn
log does not show that. `frozen_at` plus the floor's content at freeze time
does.

Undifferentiated memory would satisfy the letter of "persist the conversation"
and still fail to produce anything gradeable. The distinguishing column is the
point of the design, not an ornament on it.

### 5. Turn replay is windowed to the last N turns

*Added 2026-07-29. The original record had no concept of a replay window, which
was the largest gap in it.*

ADR-0002 windowed the corpus because loading all of it per message was
unaffordable. This ADR adds a **second unbounded prompt input and windows
nothing** — `Turn` has no retention rule, no truncation, and no cap.

The thing that hides it: `chat.js:70` resetting `history = []` on refresh is the
*de facto* window today, and this design deletes it. Per-message cost stops being
constant and becomes linear in turn index, so cumulative spend is quadratic.
Order-of-magnitude, at ~250 tokens/turn over a 36-message session on the m0
window:

| | tokens |
|---|---|
| cached prefix, 36 messages | ~238k, billed at cache-read rates |
| replayed turns, unwindowed | **~315k, uncached, full input rate** |

Replay would cost more than the corpus window ADR-0002 was written to bound —
the same mistake one layer up. And `_usage_total` bills every replayed token at
full weight against the seat (K10), so the budget drains faster the longer a
student works, which is precisely backwards for a tool meant to reward sticking
with a problem.

**Decision: replay the last N turns, N fixed and small.** Per-message cost
returns to constant, spend stays linear, and it is the same move ADR-0002
already makes on the corpus. A student wanting more scrolls their own
transcript — the full history is in the database and on their screen; the window
governs only what re-enters the *prompt*.

N is not fixed here. It should be set from the same measurement that sets the
per-seat budget, because the two are one question: what a message costs.

### 6. The frozen floor does not enter the cached system block

*Added 2026-07-29.*

`_system_blocks` emits **one** block carrying persona + notes + corpus with
`cache_control: ephemeral, ttl 1h`. Its economics depend on a property nothing
in this repo tests: the block is byte-stable for a given (skin, active module),
so **every student in a cohort shares one cache entry**.

Caching is a prefix match. Any per-seat byte inside that block gives every seat
its own entry, turning one cache write plus N reads into N writes — and 1h
writes bill at roughly 2x where reads bill at roughly 0.1x.

The trap is that this is **silent and unfalsifiable from inside the app**.
`_usage_total` counts `cache_creation_input_tokens` and
`cache_read_input_tokens` at full weight, which K10 just froze as deliberate, so
the admin page shows the identical number either way. Only the invoice moves.
The 4096-token floor guard does not catch it either — adding content only ever
*raises* the prefix, so the guard passes.

**So: any per-seat content goes in a second, uncached block after the
breakpoint.** Add the parameter to `_system_blocks` and the `get_claude_response`
family, **not** to `build_system_prompt`, whose output `test_auth.py`,
`test_claude_handler.py` and `scripts/eval_persona.py` all assert against. And
add the missing guard — assert `_system_blocks(...)[0]` is byte-identical for two
different seats — because right now the property the cost model rests on has no
test at all.

## Consequences

**Easier.** Refresh stops destroying a conversation, which is the actual stated
want. Transcripts become attributable, so they can be read and graded. The
forgery hole closes as a side effect of the server owning history. The
per-cohort budget defect is fixed by the same table that fixes identity.

**Harder.** Every chat request grows a database read on the hot path. The
budget's meaning changes, so the admin view needs rework to show seats rather
than one cohort row. `export_group_transcripts.py` has to be repointed in the
same change.

> **Correction (2026-07-29).** This said the export script "is not covered by
> any test, because it is a one-shot operator script." That is false.
> `tests/test_export_group_transcripts.py` exists — 131 lines, 10 tests, against
> a real on-disk SQLite database with two cohorts in it.
>
> The real hazard is sharper than the one this record named, and worse. Five of
> the ten build `Conversation`/`Message` rows and will break loudly. **The other
> five touch neither model and keep passing.** An implementer who deletes the
> five broken tests rather than rewriting them gets a green suite with zero
> coverage of `export_group()` — the one function that runs once, against
> production, on data that becomes unreachable immediately afterwards. Rewrite
> them; do not delete them.

**Irreversible.** Dropping `conversations` and `messages` destroys the demo
traffic and the CSC 114 pilot rows. K12 already ruled those written off, so this
executes a decision rather than making a new one — but it executes it, and a
DROP has no rollback. `preDeployCommand: flask db upgrade` means a failed
migration blocks the deploy and leaves the old version serving; a *succeeded*
migration that dropped the wrong thing does not.

**Neutral, and load-bearing.** Nothing here catches a Postgres/SQLite
divergence, because the suite runs on in-memory SQLite. That was survivable when
this ADR only ever added tables. It is not survivable now that it drops them,
which is why K15's staging rehearsal is a precondition rather than good practice.

**Now decided, having been open.** The budget's denomination: **tokens, as
`_usage_total` already counts them.** Cache reads at full weight, which is a
correct token count and a poor cost proxy — cache reads bill at roughly a tenth
of list, 1h writes at roughly double. Weighting them was the alternative and was
declined: it trades an honest count for an estimate that depends on hardcoded
pricing ratios nothing would notice going stale. The comment at
`claude_handler.py:63-75` should stop reading as an open question. See **K10**
(this previously said K8, which is the session-boundary entry).

### Tests this will break, when implemented

- `system1-flask-chat/tests/test_routes.py:20` and
  `system1-flask-chat/tests/test_skins.py:24` — both `_login` helpers post only
  `{'password': …}`. **Counted, 2026-07-29: 15-17 collected items, not "roughly
  twenty."** Fix the two helpers rather than making the field optional; an
  optional identity field is not an identity. Two more corrections to what this
  said:
  - `test_skins.py:193` posts a login **directly**, not through the helper, so a
    search-and-replace on `_login` misses it. It then fails on
    `assert r.status_code == 302` and reports a cookie-limit regression that is
    really a missing handle.
  - **Two of them rot rather than break**, which is the dangerous half.
    `test_cross_skin_session_redirects_to_correct_skin_login` and
    `test_cross_skin_api_chat_is_gated` log into csc114 and assert csc134
    rejects them. If the login silently fails for want of a handle,
    `session['skin']` is never set, the second request is simply
    unauthenticated, and every assertion still passes. Two cross-skin isolation
    guarantees go green while testing nothing.
- `system1-flask-chat/tests/test_models.py` — **the blast radius is the whole
  file, not two tests.** Lines 2-5 import `Conversation` and `Message` at module
  scope, so deleting those models is a pytest *collection error*: the run aborts
  and every other file's results go dark with it. Also rehome the `token_budget`
  assertions to `Seat` — five move cleanly;
  `test_default_budget_survives_the_most_expensive_module` asserts a
  cohort-sized arithmetic premise that becomes false per-seat and needs
  rewriting, not moving.
- **Correction: no test asserts request-supplied history reaches
  `claude_handler`.** Zero. Every route test posts `'history': []`, so nothing
  would notice the routes ceasing to read it. This is worse than a broken test,
  not better — the fix has no failing test to turn green and no regression test
  unless one is written first.
- The `inspect.signature` bind (`test_skins.py:74-80`) is loud on the wrong
  axis. It catches a renamed, reordered or added parameter. It does **not**
  catch server-loaded turns arriving in the same `history` positional slot that
  request-supplied ones used to occupy — same name, same position, binds
  cleanly, and the assertions that follow never read `history`. True for the
  shape, false for the content.

### Implementation notes for whoever picks this up

- **Correction (2026-07-29): the SSE premise this record was built on is false.**
  It said the generator body "runs after the request context is torn down."
  `routes.py` wraps the generator in `stream_with_context`, which exists to
  prevent exactly that; verified on this Flask 3.0.0 that `session`, `request`
  and the DB all work inside it, and the generator already proves it by running
  `Group.query` and `db.session.commit()`.

  Hoisting is still right, for a different reason: returning `Response()`
  commits the status line, so nothing inside `generate()` can emit a 403 or 409,
  and `session` mutations inside it never reach a `Set-Cookie`. **Anything that
  decides whether to answer at all — the budget check, seat resolution, an
  exhausted-seat rejection — must happen above the response.** Someone
  implementing against the old stated reason would assume `session['seat_id']`
  is unreadable in the generator (it is not) and leave the budget check inside,
  where a 403 silently becomes an SSE error event.
- Both chat paths must stop reading `data.get('history')` entirely. Ignoring it
  is what closes the forgery hole; validating it is not.
- `chat.js` history becomes display-only, hydrated on load from a new
  `GET /<slug>/api/history`.

## Alternatives Considered

**Browser-durable memory with no identity** (server-side session key, no
handle). Solves "don't reinvent the wheel" with the least work and touches
identity not at all. Rejected because it produces no attributable transcript, so
it does not unlock the gradebook — and the gradebook is the reason the capstone
needs this rather than a nicer chat box.

**Persist everything symmetrically** — replay all prior turns, frozen or not.
Simpler, and it is what "add memory" usually means. Rejected for the reason in
§3: it manufactures consent across a session boundary, and it produces a turn
log rather than a record of freeze events.

**Add columns to `Conversation` and `Message`.** The smaller diff.

> **Amended 2026-07-29.** Originally rejected as *impossible*: `create_all()`
> cannot apply it to a live database, and the failure mode is a production
> `UndefinedColumn` no test can catch. ADR-0006 removed that objection entirely,
> so this was reconsidered on merit and rejected again for weaker but sufficient
> reasons — `Message` has no `seq` and no ordering guarantee, `Conversation` has
> no `frozen_at`, and reaching the target shape takes several ALTERs against
> live Postgres where three CREATEs would do. Recorded as a preference now, not
> an impossibility, so that a future reader does not inherit a certainty this
> record no longer has.
