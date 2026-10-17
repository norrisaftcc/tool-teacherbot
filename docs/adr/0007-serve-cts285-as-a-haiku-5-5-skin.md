# ADR-0007: Serve CTS 285 as a Haiku 5.5 skin

- **Status:** Proposed
- **Date:** 2026-10-17
- **Deciders:** norrisaftcc (product), Claude Code (implementation). The instructional lead's
  confirmation of the graded-work line (K21) is **not yet given**; see Consequences.
- **Supersedes:** nothing. Extends ADR-0001 (skins) and ADR-0002 (persona and windowed corpus).

## Context

CTS 285 (Systems Analysis & Design) needs a course tutor. The students rebuild DataMan, a 1977 Texas
Instruments learning device, as one project across Modules 0 to 8, and keep their evidence in their
own GitHub repositories at exact paths. The course lead chose Claude Haiku 5.5 and asked that the
tutor teach from student-visible course material only.

What the code did before this change, measured on `main` @ `2605767`:

- **Skins are a dict, and auth is passcode-only.** `auth.py` `SKINS`, `authenticate_skin(slug,
  password)`. One `password` input on the login page.
- **The corpus loader reads `*.md` only.** The CTS 285 pages are HTML Canvas fragments with inline
  styles, so vendoring them raw would put none of their text in the prompt, and extending the loader
  to read HTML would roughly double the tokens, because the inline styles ride along.
- **The corpus sync clones a git URL** and cannot reach a private repository without credentials. The
  CTS 285 source is private. It also had no way to rewrite paths, convert file types, or refuse a
  path outright.
- **The non-stream path read `response.content[0].text`.** On Haiku 5.5 the model thinks by default,
  and a response can begin with a `thinking` block. That read raises or returns empty, and it breaks
  `/api/chat` and `scripts/eval_persona.py`. The stream path yields `text_stream` only, which is safe,
  but it ignored the final `stop_reason`, so a `refusal` showed as an empty bubble.
- **One output ceiling and one key for every skin.** `MAX_TOKENS = 2048`; one global
  `Anthropic(api_key=...)`. Thinking counts against `max_tokens`.
- **The client supplies the history, unbounded and unvalidated** (`routes.py`, `static/js/chat.js`).
  ADR-0004 section 5 decides to cap it at N turns and has not been implemented.
- **`Group.token_budget` is `db.Integer`**, which is int4 on Postgres (maximum 2,147,483,647), and
  `raise_budget_floor()` lifted every group to the global 25M default, so a smaller per-skin budget
  would have been raised back on the next login.
- **The templates are AlgoCratic for every skin**: classification banner, clearance chips, "The
  Algorithm is watching". CTS 285 course rules keep fiction off instructional surfaces, and the tutor
  is out of character.
- **ADR-0004 is Accepted and not implemented.** There are no `Seat` or `Turn` tables, so there is no
  per-student identity, per-seat budget or server-side memory for any skin.

Facts about Haiku 5.5 in this ADR (rates, the cache floor, the tokenizer ratio, "rejects non-default
sampling", "thinks by default") come from the Anthropic `claude-api` reference bundled with the
authoring tool, model table cached 2026-10-06. **They were not re-verified against the live pricing
page or the live API, and there is no API key in the authoring session.** Treat each as a claim to
check before the deploy, not as a measurement.

## Decision

Add a fourth skin, `cts285`, on `claude-haiku-5-5`, that changes only what it needs to change and
leaves `csc114` and `csc134` byte-for-byte as they were.

### 1. The skin entry and its new optional keys

`SKINS['cts285']` in `auth.py` follows the existing shape, with a `username` and these new optional
keys. `Skin` becomes a required-keys `TypedDict` plus a `total=False` subclass, so the other two
skins carry none of them. **Omission of a key means "behave exactly as today".**

| Key | Value | Why it exists |
|---|---|---|
| `username` | `CTS285_USERNAME`, default `CTS285` | The course lead asked for a username and a password. `authenticate_skin(slug, password, username=None)` checks the username only when the skin declares one. It ignores case and surrounding whitespace. The password is exact. Both use `hmac.compare_digest` and both always run. |
| `password` | `CTS285_PASSWORD`, default `algorithm` | Same reason as `CSC134_PASSCODE`: this repository is public, so rotation is a dashboard edit. `or`, not a `getenv` default, because a blank dashboard field sets the variable to `''`. |
| `model` | `claude-haiku-5-5` | The course lead's decision. |
| `chrome` | `neutral` | Templates branch on it: no classification banner, clearance chip or "The Algorithm is watching", and a plain title. The root picker is unchanged, and students get the direct URL `/cts285/`. |
| `max_tokens` | 4096 | Thinking counts against `max_tokens`, so the answer needs room beside it. |
| `request_options` | `{'output_config': {'effort': 'low'}}` | Effort is the documented lever for chat on Haiku 5.5. It is **not sent to a skin that does not declare it**, because Haiku 4.5 (csc134) rejects it. `_request_kwargs` raises on a key that collides with one the handler owns. |
| `history_messages` | 10 | Uncached input is the only part that grows per message. |
| `max_message_chars` | 6000 | A longer message is a 400 before any API call. |
| `token_budget` | `CTS285_TOKEN_BUDGET`, default 2,000,000,000 | See section 3. |
| `api_key_env` | `CTS285_ANTHROPIC_API_KEY` | The course lead's monthly credits should fund CTS 285 only. With the variable set, to a key in a dedicated Anthropic workspace, the spend and the cache namespace separate from csc134. **If the variable is unset, the shared client answers**, on shared credits, rather than 502 every student. |

Also: `claude_handler._response_text` joins the `text` blocks instead of reading `content[0]`; a
`stop_reason == 'refusal'` yields a fixed out-of-character line on both the stream and the non-stream
path; for a `neutral` skin an API failure shows the student a fixed message and logs only the
exception type, where the other skins still show the SDK message (unchanged).

### 2. The corpus is student-visible material only, manifest-driven, and guarded by a deny list

`scripts/cts285_manifest.yaml` is an **explicit file allow-list**. It has no directory entries, so a
file added upstream is not vendored until someone lists it. It carries:

- `map:` ordered prefix rewrites (`module-02/final-build/` to `modules/m2/`, and so on). The DataMan
  manual maps to `reference/` and is the always-on `corpus_index`.
- `transforms:` `.html` to Markdown, `.py` and `.txt` fenced. Output is `<stem>.md`; fenced files
  keep their extension (`app.py.md`).
- `deny:` a **hard guard, separate from `exclude`**. `exclude` silently skips. `deny` **raises and
  writes nothing**, because a denied path in `paths` means the allow-list is wrong. It denies
  `build-guides/`, `instructor-guides/`, `planning/`, `reference/`, `review-target/`, `exemplars/`,
  `failure-variants/`, `binder/`, `assignments/`, `assessments/`, rubrics, answer keys, the module
  architecture records, `AGENTS.md`, `CLAUDE.md`, and the five retired M2 elicitation-case branch
  pages. A test over the vendored files **on disk** fails when a denied path is present.
- `--source <path>` on the sync script: read a local clone of the private upstream instead of
  cloning. The sync records the source commit SHA in `context/cts285/_provenance.txt` (not `*.md`, so
  it never reaches the prompt).

The corpus windows as ADR-0002 decides: `corpus_index` (the manual) plus one `active_module`, default
`m4`, advanced by `CTS285_ACTIVE_MODULE`. Estimated window sizes at bytes/4 run from about 14k tokens
(m0) to about 27k (m2, m6) before the persona, header and notes. That clears the 4096-token cache
floor by several times and stays well under the 100k-token rate-card threshold.

The persona is `context/cts285_persona.md`, written out of character. Its central rule is the
graded-work line recorded as **K21**: the tutor may quote what the course gives (blank templates,
page instructions, the worked examples and reveals, the manual, the M5 starter, paths and ID
schemes), and it does not write what the student submits about their own DataMan work or the code
beyond the starter.

### 3. The budget is a per-skin circuit breaker, not a per-seat budget

`token_budget` is in the K10 unit (tokens as `_usage_total` counts them, cache reads at full weight).
At about 44k counted tokens per message the 25M global default is only about 570 messages for the
whole cohort, so the skin declares 2.0e9, about 45k messages and about $50 of Haiku 5.5 spend at the
unverified rates. It stays **under the int4 maximum, so no migration is needed**. A budget at or
above 2**31 - 1 raises at import, and an env override is validated with the variable's name in the
message, because SQLite (the test database) accepts the value Postgres would reject at the first
INSERT. `raise_budget_floor()` takes the floor as a parameter and `do_login` passes the skin budget,
so a skin budget is neither lowered nor raised past what the skin declares.

### 4. Guards

The cts285 window guards compose through `_system_blocks` (the cached block, **with** the teaching
notes) rather than the way the csc134 guard in `test_auth.py` does, so they measure what production
sends. They keep the conservative 4096-token floor the course lead asked for, enforce a ceiling under
the 100k rate-card threshold, and **fail rather than skip** when the corpus is missing. A byte
stability test asserts that two logins with different histories send an identical `system` argument,
because nothing guarded that before. A request-shape test asserts that `output_config.effort` is
present for cts285 and absent for csc134 and csc114, and that no sampling parameter is sent.

## Consequences

**Harder or worse:**

- **No per-student identity.** One shared username and password per cohort. K9 (identity is a
  declared GitHub handle) and ADR-0004's seat model are **unmet** for this skin. Transcripts are
  keyed to the group, not to a student, so they cannot be graded and one student can spend the
  cohort's budget. The per-skin budget bounds the worst case; it does not apportion it.
- **History forgery is still possible.** The client still supplies the history, and a client can
  claim the assistant said anything inside the window. `history_messages` bounds cost, not trust.
  This implements the cost half of ADR-0004 section 5 for this skin only.
- **The corpus is published in a public repository.** The vendored pages are the course's own
  student-visible material, and `reference/18-the-dataman-manual.md` is a full transcript of the 1977
  Texas Instruments manual. Whether that redistribution is acceptable is a question for the course
  lead, not settled here. Removing it is one manifest line, at the cost of weaker DataMan grounding.
- **The source is the course's development copy, not the live cohort's Canvas.** Some live pages
  differ (the source records a 2026-10-08 export check). The cohort header tells the tutor and the
  student so; a student who quotes a difference is told to believe the page they see and ask the
  instructor. The tutor is as stale as the last sync, and the sync is a manual command.
- **The graded-work line (K21) is the tutor's whole safety property, and it is wording.** A persona
  rule holds back a model less reliably than a file that is not vendored. That is why the deny list
  exists and why the persona is not the only control. The behaviour bank is triage, not a verdict
  (K3).
- **Haiku 5.5 semantics are new to this code and unexercised against the real API.** Thinking blocks,
  `refusal` stop reasons and `effort` are handled as the reference describes them. No live call was
  made in the authoring session. The first live run is the first evidence that `effort: low` leaves
  enough `max_tokens` for the answer.
- **Rates and the cache floor are unverified** (see Context). The 4096 guard is conservative whether
  the real floor is 512 or 4096.
- **The deploy target is still undetermined.** See `DEPLOY.md`; this ADR does not change that.

**Easier:**

- The other two skins are unaffected, and a test asserts they carry none of the new keys.
- A second cohort of CTS 285, or a second Haiku 5.5 skin, is a dict entry, a persona and a manifest.
- Spend can be separated by workspace (`CTS285_ANTHROPIC_API_KEY`) without a code change.

**Partly addresses:** backlog B2 (SHA-pin the corpus sync) for local-source syncs only. A `--source`
sync records the SHA it read. A sync that clones still tracks a moving branch and records no SHA.

**Open decisions this ADR does not make:** whether the instructional lead confirms K21; which module
the live cohort is in (the `active_module` default is `m4`); whether a separate Anthropic workspace
is created; whether the public redistribution of the manual stands.

## Alternatives Considered

- **Per-student passcodes or seats now.** Right eventually, and what ADR-0004 decides. Rejected for
  this change because it needs the `Seat` and `Turn` tables and a migration rehearsed on staging
  (K15), and the course lead's decision was one test login for the first release. The shared login
  is the cost, listed above.
- **Vendor the raw HTML and extend the corpus loader to read it.** Rejected: the inline styles would
  roughly double the tokens per window, and the loader's `*.md` rule is the property ADR-0002 relies
  on. Converting at sync time keeps the loader unchanged.
- **Send the whole corpus.** Rejected: the whole CTS 285 corpus is far above the 100k-token rate-card
  threshold at which input is billed at five times the rate, and ADR-0002 already decides against it.
- **A new migration for a `BigInteger` budget column.** Rejected: unnecessary under 2.0e9, which fits
  int4. It would also put a migration on the critical path of an unverified deploy (K15).
- **A directory-glob manifest with an `exclude` list.** Rejected: it fails open. A file added
  upstream, such as an answer key beside a page, would be vendored silently. The explicit allow-list
  fails closed, and `deny` turns a mistake in it into an error.
- **Reuse the AlgoCratic chrome.** Rejected: CTS 285 rules keep fiction off instructional surfaces,
  and the tutor is out of character by design.
- **Lower `effort` handling by disabling thinking.** Rejected: the reference says to use effort as
  the lever for chat rather than turning thinking off.
