# ADR-0004: Seat identity, server-side memory, and the session boundary

- **Status:** Proposed
- **Date:** 2026-07-28
- **Deciders:** norrisaftcc (product), Claude Code (implementation)

## Context

The stated direction is memory: students should be able to talk to the
interface without reinventing the wheel every time. The capstone this system
was built for is weeks off, and it is the first cohort that will be *assessed*
on how it works with an agent.

Three facts about what exists today, all verified against the code.

**1. There is no memory. There is a page variable.**

`static/js/chat.js:7` is `let history = []`. The browser holds it, the browser
sends it (`chat.js:26`), and `routes.py:146` and `routes.py:197` read it back
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

### The constraint that forces this decision now

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

### 2. Three new tables, and no change to any existing one

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

All three are new, so `create_all()` builds them on deploy with no migration.
`Group`, `Conversation` and `Message` are untouched and become the legacy log.

Adding `student_id` to `Conversation` instead would be an ALTER on a live table
with no migrations framework — the exact production landmine described above.
Reusing `Message` fails for the same reason: it needs `seq`.

**The budget moves to `Seat`.** This fixes a defect that exists today
independently of memory: the pool is per-cohort, so one verbose student can
exhaust the class. It comes free with the new table, and it matters more once
memory is replayed, because replay raises per-message spend against that same
shared pool.

**The legacy rows.** `conversations` and `messages` currently hold demo traffic
plus the finished CSC 114 pilot. Default is *retain, unused*. Dropping them is
cheap and they have no obvious retention value, but that is the course lead's
call, not this record's — see K10.

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

## Consequences

**Easier.** Refresh stops destroying a conversation, which is the actual stated
want. Transcripts become attributable, so they can be read and graded. The
forgery hole closes as a side effect of the server owning history. The
per-cohort budget defect is fixed by the same table that fixes identity.

**Harder.** Every chat request grows a database read on the hot path. The
budget's meaning changes, so the admin view needs rework to show seats rather
than one cohort row. Two dead tables sit in the schema until someone rules on
K10.

**Neutral, and load-bearing.** Nothing here catches a Postgres/SQLite
divergence, because the suite runs on in-memory SQLite. This design avoids
migrations by only ever adding tables — but that only works once. Alembic must
land before the capstone produces transcripts anyone intends to grade, because
the second schema change will not have this escape hatch.

**Deliberately not decided here.** Whether the budget is denominated in tokens
or dollars. `_usage_total` counts cache reads at full weight, which is a correct
token count and a poor cost proxy — cache reads bill at roughly a tenth of list,
1h writes at roughly double. Picking a denomination needs a real measurement,
not an inherited constant. See K8.

### Tests this will break, when implemented

- `system1-flask-chat/tests/test_routes.py:20` and
  `system1-flask-chat/tests/test_skins.py:24` — both `_login` helpers post only
  `{'password': …}`. If the handle is required, roughly twenty tests 302 to
  login instead of reaching `/chat`. Fix the two helpers rather than making the
  field optional; an optional identity field is not an identity.
- `system1-flask-chat/tests/test_models.py` — `token_budget` assertions need
  rehoming to `Seat`.
- Any test asserting request-supplied history reaches `claude_handler`. The
  model-routing tests bind arguments via `inspect.signature`
  (`test_skins.py:74-80`) and will surface a changed call shape immediately.

### Implementation notes for whoever picks this up

- `routes.py:207-212` already documents the hazard: the SSE generator body runs
  after the request context is torn down, which is why context, persona and
  notes are read *outside* `generate()`. Turn loading must follow the same rule,
  and the seat id must be captured outside the generator too.
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

**Add columns to `Conversation` and `Message`.** The smaller diff. Rejected
because `create_all()` cannot apply it to a live database, and the failure mode
is a production `UndefinedColumn` that no test can catch.
