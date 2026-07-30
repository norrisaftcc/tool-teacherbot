# ADR-0005: Repoint the csc114 slot to the Prompt Wizard

- **Status:** Proposed
- **Date:** 2026-07-28
- **Deciders:** norrisaftcc (product), Claude Code (implementation)

## Context

CSC 114 has finished. Its skin is still registered, still serving, and still
holding a passcode (`2026su`) that is published in this public repo. CSC 134 is
a Fall cohort. The capstone this system was originally built for is weeks off,
and it is the near-term target.

The product direction for that capstone is a **Prompt Wizard**: teacherbot
teaching The Algorithm itself, running the PROVIDE and ASSAY operations —
"wizard" in the older sense, one who holds a great deal of knowledge.

Two things make the csc114 slot the right place to put it rather than a third
skin.

**The persona in that slot is already the capstone persona.**
`system1-flask-chat/context/csc114_persona.md` opens:

> You are an AI teaching assistant for the AlgoCratic Futures capstone course.

and its rule 4 is *"Emphasize the Sacred Workflow: Issue → Branch → PR → Review
→ Merge"* — a fixed sequence you must pass through in order, which is a
proto-gate. That file was lifted out of `claude_handler` by ADR-0002 and given a
cohort name it never really described. The slot has been the capstone slot
wearing a CSC 114 label since it was created.

**A third skin would be a third always-on prompt to maintain** for a course that
no longer runs, while the registry already carries two entries and the second
one is dead.

## Decision

### 1. The csc114 registry entry becomes the Wizard skin, under the slug `algorithm`

`SKINS['csc114']` is replaced, not supplemented. The surface is the Wizard, so
name it for the surface: a cohort name ages out (as `csc114` just did) and the
protocol does not. `capstone` was the alternative and is rejected for that
reason — there will be more than one capstone.

The csc114 corpus stays vendored on disk as the historical record. Nothing
serves it.

### 2. Sonnet, not Haiku

PROVIDE runs a compression loop with a gate condition; ASSAY reads a document
and locates its operative sentence. Both are harder than answering a `cout`
question. CSC 134 is on Haiku because a first-year cohort's binding constraint
is cost; a capstone cohort is small enough that it is not.

### 3. The protocol is always on, never windowed

`corpus_index: ['SKILL.md']`, and the register alongside it. `active_module` is
`None`, which `auth.py:86-88` already handles.

Same reasoning `auth.py:58-61` gives for csc134's teaching notes: guidance that
applies in every module is worthless the one week it is absent. ADR-0002's
windowing exists to keep a 424 KB course corpus out of the prompt; the doctrine
is small and load-bearing in every exchange, so it is index material, not module
material.

### 4. The corpus is vendored with no substitutions, and that is a hard rule

`scripts/algorithm_manifest.yaml`, modelled on `csc134_manifest.yaml`:
upstream `https://github.com/norrisaftcc/the_algorithm`, target
`system1-flask-chat/context/algorithm`, paths `SKILL.md` and `registry/`.

csc134's manifest rewrites vendored markdown to neutralise links into upstream
directories that do not exist in the vendored subset. **That mechanism must not
be pointed at this corpus.** Fixed strings in the doctrine are byte-exact
contracts. A regex that edits one breaks the contract silently, the bot then
emits a string that does not match the one the eval asserts, and the failure
reads as a model problem rather than a vendoring problem — the most expensive
kind of bug this system can have, because it sends you looking in the wrong
place.

Add an assertion in `tests/test_sync_course_corpus.py` that this manifest
declares no substitution.

### 5. SHA pinning is a prerequisite, not a follow-up

`sync_course_corpus.py:33-38` runs `git clone --depth 1 --branch <ref>`, which
**cannot take a bare commit SHA**, and no provenance SHA is recorded after a
sync. Every manifest therefore tracks a moving branch.

Vendoring byte-exact contracts from a floating `main` means an upstream edit
changes the contract underneath a running eval with no signal at all. Rework
`fetch_upstream` — clone, then `git fetch origin <sha> && git checkout <sha>` —
and record the resolved SHA in the target, **before** the first algorithm sync.

This is not only an `/algorithm` problem. It protects csc134 too:
`test_auth.py` records that the thinnest module windows (m3, m5–m7) clear
Haiku's 4096-token cache floor by only 163–728 tokens, and Haiku declines to
cache a shorter prefix silently, with no error. Upstream drift can disable
caching without anything failing.

### 6. The persona resolves a voice conflict, in favour of the doctrine

`context/algorithm_persona.md` and `algorithm_context.md` are both required —
`auth.py:194-199` and `auth.py:239-243` raise `FileNotFoundError` without them,
surfaced at login by `routes.py:101-112` rather than mid-chat.

There is a real conflict to settle. The AlgoCratic voice softens: *"growth
opportunity" not "error"*, *"suboptimal" not "wrong"*. The Algorithm's language
lock is ASD-STE100 — one word per meaning, active voice, and *call errors
plainly*. These are opposite instructions.

**The doctrine's voice wins.** Teaching a discipline in a register that violates
it is self-refuting; a student learning to strip cushioning from their own
prompts should not be reading cushioned output while they do it.

`system1-flask-chat/tests/test_auth.py::test_csc114_persona_preserves_algocratic_voice`
asserts the old voice and will break. That break is the decision landing, not a
regression.

### 7. Modes are recognised, not selected

No mode selector in the UI. The operation is named in the prompt and the persona
recognises it — which is how the doctrine works, and it keeps the surface
identical to the one students already use.

`Exchange.mode` (ADR-0004) records which operation an exchange is in, set on
first recognition and immutable thereafter. The gradebook gets the mode; the
student does not get a dropdown to fiddle with.

### 8. Fixed strings give the eval harness its first real verdict

This is the part with the most leverage, because it removes a limitation the
harness already confesses to. `scripts/eval_persona.py:154-163`:

> *The flags above catch failures with a shape... They cannot catch a confident
> false statement about the language... Checking that needs C++ knowledge, and a
> checker with C++ knowledge is another model that can also be wrong. So: flags
> narrow the reading, they do not replace it.*

A pass condition of *"ends with exactly `This is a finding, not a draft.`"*
needs no domain knowledge and no second model. It is
`answer.rstrip().endswith(FIXED)` — exact, cheap, and not an approximation. For
the first time the harness can produce a **verdict** rather than triage.

Concretely:

- A `fixed-string` item type in `evals/algorithm/`, carrying the expected string.
- A branch in `flags_for()` (`eval_persona.py:132-151`), commented as the only
  non-approximate check in that function — the file already keeps that kind of
  register and it should stay honest.
- `tests/test_eval_persona.py:13`'s `REQUIRED` key set needs the new field.

**And `--runs N`.** `eval_persona.py:187` runs each item exactly once, and
`evals/csc134/m0.yaml` already records why that is wrong:
`observed_variance: m0-02: 1 of 3 runs produced a code skeleton`, with the note
*"a real gate needs N runs and a rate, not one sample."* A byte-exact contract
is what makes a rate meaningful: 3/3 against 2/3 on a fixed string is a fact,
not a judgement call. Smallest change in this record, largest effect, and the
bank asked for it in writing.

## Consequences

**Easier.** The dead cohort leaves the registry along with its published
passcode. The Wizard reuses `SKINS` and `skin_blueprint` wholesale — a skin is
~20 lines of registry plus two context files. The eval harness gains a check
that decides rather than hints.

**Harder, and this is the real cost.** Roughly twenty tests across
`test_auth.py`, `test_routes.py` and `test_skins.py` use `csc114` as the
*vehicle* for testing skin machinery — model routing, cookie size, picker
rendering — not as a cohort. Renaming the slug is mechanical but wide, and the
rename must not quietly delete that coverage: each of those tests should end up
exercising the same machinery under the new slug.

`test_skins.py::test_root_picker_lists_both_skins` asserts `/csc114/` appears in
the picker and will break deliberately.

**The loss to plan for.** Once no skin serves `csc114`, `/csc114/admin` stops
existing and the pilot's transcripts become unreachable — the `Group` row stays
in Postgres with no route to it. Export before the repoint lands, not after.

**Neutral.** The csc114 corpus stays on disk, vendored and unserved. It costs
152 KB and answers "what did the pilot actually run" without a database query.

## Alternatives Considered

**A third skin at `/algorithm`, keeping csc114 registered.** Cleanest diff, no
test churn, and it was the recommendation before the course lead confirmed CSC
114 had finished. Rejected because it leaves a dead cohort and a published
passcode serving live traffic, and because it treats the capstone persona
already sitting in the csc114 slot as if it belonged to CSC 114.

**PROVIDE/ASSAY as modes inside the csc134 skin.** Rejected on three counts.
The persona would collide — `csc134_persona.md` is deliberately narrow (Mail
Run, no pull requests, no forward pointers in week 1), and bolting doctrine onto
it recreates the exact defect ADR-0002 was written to fix, one layer up. The
cost is wrong — the persona sits inside the cached prefix and is billed on every
message for every student, and `csc134_teaching_notes.md` earned its place with
a measured result while no comparable evidence exists for Algorithm vocabulary
in a `cout` answer. And it contradicts `the_algorithm`'s K17, which scopes gate
authority to late
capstone: week-1 first-years are the far end of the linear-implementor side, so
teaching them to hold a gate implements the opposite of what the register says.

**Keep `csc114` as an archived, hidden skin.** Preserves the ~20 tests and the
admin route. Rejected because an archived skin is a permanent maintenance
surface for a course that will not run again, and because the slot is needed.
The historical record is the vendored corpus and the exported transcripts, not a
live route.
