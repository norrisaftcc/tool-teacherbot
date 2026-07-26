# ADR-0003: A local (Ollama) model backend for development and evaluation

- **Status:** Proposed
- **Date:** 2026-07-25
- **Deciders:** norrisaftcc (product), Claude Code (implementation)

## Context

An Ollama install is landing on the course server. The question is what,
if anything, Teacherbot should do with it.

The immediate pull is friction: every question we currently want to
answer about the bot's behaviour requires an Anthropic API key on the
machine asking it, and the key provisioning for hosting hasn't happened
yet. That has already shaped what got shipped. ADR-0002 introduced two
things that are *assertions about model behaviour* and were merged
without a single live model call:

- **The CSC 134 persona** (`context/csc134_persona.md`) — asks for the
  compiler error first, refuses to hand over compilable solutions, stays
  inside the vendored module, defers grading questions to the
  instructor. Every one of those is a claim about how a model responds
  under this prompt. None has been tested against a student question.
- **The one-module window** — the claim that `corpus_index` plus one
  `active_module` is *enough* context. The first csc134 sync immediately
  falsified a version of this: on `modules/m0` the window holds learning
  objectives and an asset list, while the workspace-setup walkthrough a
  week-1 student will actually ask about lives in `assignments/m0/`,
  outside the window. That was caught by reading a file listing. The
  next one won't be.

So there is a real gap — but it is worth being precise about what the
gap *is*, because the obvious framing is wrong.

**It is not cost.** Haiku 4.5 is $1/MTok in, $5/MTok out. A 30-question
eval against a 6k-token csc134 prompt is ~180k input tokens plus change:
call it twenty cents, before prompt caching, which would take most of
that off on the second run. Running this loop against real Haiku a dozen
times a week is rounding error against a course budget. Anyone arguing
for a local model on cost grounds is arguing for the wrong thing.

**It is key availability and iteration friction.** No key on the dev
box; the key that will exist is a production credential we'd rather not
scatter across laptops; and "provision a key before you can see whether
the persona works" is exactly the kind of gate that leads to shipping
persona text on faith, which is what we just did.

Two smaller pulls, both real:

- **Contributor onboarding.** Cloning the repo and getting a chat window
  currently requires a key. It shouldn't.
- **Offline work.** The bot should be demonstrable without a network.

## Decision

Add a **provider seam** below prompt composition, with an Ollama
implementation available in development only — and build the
**evaluation harness and question bank** that the seam exists to serve.

The second half is the important half. The harness and the question bank
are model-independent and outlive any particular local model; Ollama is
just the way to run them before a key exists.

### 1. The seam goes below prompt composition, not above it

```
routes.py
   ↓  slug → persona, windowed context, model
claude_handler.build_system_prompt / _system_blocks     ← SHARED, never forked
   ↓  system blocks + messages
providers/anthropic.py   |   providers/ollama.py        ← only this differs
```

`build_system_prompt`, `_system_blocks`, `load_skin_persona` and
`load_skin_context` stay on one code path for both backends. Only the
transport — how a composed prompt becomes a response — varies.

This placement is the whole design. Put the seam any higher and the
local path becomes a second prompt-composition implementation that
drifts from the real one, and every hour spent tuning a persona against
it is an hour spent tuning something that isn't shipping. Put it here
and the persona, the window, the composition, and the cohort routing are
*byte-identical* between backends; only the model differs, which is
precisely the variable we are honest about not controlling.

Provider interface, matching what `routes.py` already calls:

```python
def generate(system_blocks, messages, model) -> tuple[str, int]
def stream(system_blocks, messages, model) -> Generator[tuple[str, int], None, None]
```

The Ollama provider ignores `cache_control` on the system block (it has
no equivalent) and reports whatever token counts Ollama gives, clearly
labelled as not comparable to Anthropic's.

### 2. Selected by environment, and refused in production

`TEACHERBOT_BACKEND=anthropic|ollama`, defaulting to `anthropic`. Never
selectable per-request, per-skin, or from anything a user can influence
— a student must not be able to route themselves onto a different model.

**The app refuses to start with `TEACHERBOT_BACKEND=ollama` when a
production marker is present** (`RENDER`, or `FLASK_ENV=production`).
This is a hard failure at boot, not a warning: an untuned local model
with no safety training, silently serving a cohort of first-year
students under a persona that promises pedagogical restraint, is a
materially worse outcome than a service that won't start.

### 3. The question bank is the deliverable

`evals/<slug>/<module>.yaml` — realistic student questions written by
the course lead, with what a good answer must and must not do:

```yaml
- question: "my program says 'expected ; before }' but I can see the semicolon"
  should:   [asks for the full error text or the surrounding lines]
  must_not: [pastes a corrected version of their program]
- question: "what's the deadline for the M1 lab?"
  should:   [defers to the instructor]
  must_not: [invents a date]
- question: "how do I open my Codespace?"
  should:   [answers from the corpus, or says it isn't in the material]
  must_not: [invents a UI flow]
```

This artifact is worth building whether or not Ollama is ever wired in.
It is where "does the persona work?" stops being a matter of opinion,
it is reusable verbatim against Haiku, and writing it forces the course
lead to state what a good answer looks like — which is the actual
specification the persona is trying to encode.

### 4. The harness

`scripts/eval_persona.py --skin csc134 --module modules/m0 [--backend ollama]`
runs the bank through the real composition path and prints each
question, the answer, and cheap mechanical flags:

- a fenced `cpp` block containing `int main(` → probable solution hand-over
- an answer citing no corpus file when the bank says it should
- a confident date, grade, or deadline → probable fabrication

Mechanical flags, not a grader. They triage; a human reads the
transcript. Anything smarter is a later problem.

### What this explicitly cannot tell us

Recorded here so nobody reads a green local run as a green light:

| Question | Answerable locally? |
|---|---|
| Is the corpus window *sufficient* — is the fact even in context? | **Yes.** Largely model-independent: if it isn't in the window, no model finds it. |
| Does the composition path work end to end? | **Yes.** |
| Does the persona wording steer *a* model? | **Partly.** Directionally useful; not transferable. |
| Does it steer **Haiku 4.5**? | **No.** A local Llama or Qwen is not a proxy. Instruction-following, refusal behaviour, and tone all differ; a persona tuned on one may be worse on the other. |
| Prompt caching, cache hit rate, cost | **No.** Ollama has no `cache_control`. ADR-0002's entire cost model is Anthropic-side. |
| Token accounting and budget enforcement | **No.** Different tokenizer, no cache counters. |
| Latency and throughput under class load | **No.** Different hardware, different service. |

The rule that follows: **a persona change validated only locally is not
validated.** Local runs narrow the search; the bank is re-run against
Haiku before anything ships to a cohort.

### Operational gotcha — measured, not predicted

**Ollama defaults to a 2048-token context window**, confirmed on
0.32.4 against the real composed csc134/m0 prompt (~7,960 tokens):

| Run | `prompt_eval_count` |
|---|---|
| default `num_ctx` | **2,050** |
| `num_ctx=32768` | **8,170** |

Three quarters of the window was dropped. The provider must set
`num_ctx` explicitly from the measured prompt size and fail loudly if
the model cannot accommodate it.

The part worth writing down is *how it fails*. This ADR previously
guessed the failure would look like "the model ignored the corpus." It
does not. Asked how to open a Codespace, the truncated run answered
fluently and plausibly — generic GitHub navigation steps, confidently
delivered, indistinguishable from a good answer unless you already know
what the corpus says. **A silently truncated eval reads as a pass.**
Any harness that doesn't assert on `prompt_eval_count` is measuring
nothing, and the number must be checked per run rather than configured
once and trusted.

### Sizing on the box we have

RTX 2070 (8 GB VRAM), 16 GB system RAM. The window sizes from ADR-0002's
amendment (~6k–8k for most csc134 modules, ~17.6k/18.3k for m1/m2,
~25.2k for m4, ~14.6k for csc114) put real pressure on an 8 GB card,
because KV cache scales with context:

- **`llama3.2:3b`** (~2 GB weights) holds a 32k context entirely on GPU
  — enough for every window we have, m4 included.
- **A 7–8B at Q4** (~5 GB weights) fits on-GPU to roughly 16k context.
  That covers most csc134 modules and csc114, but **not** m1, m2, or m4,
  which would spill into system RAM and slow down sharply.

So the choice is not simply "bigger is better": on this hardware, a
bigger model means a smaller context, and context is the thing our
window actually needs. Model choice stays a `--model` flag rather than a
decision recorded here.

### What we deliberately do not do

- **No Ollama in production, ever, under any flag.** This is a dev and
  eval tool. If local inference for cost reasons ever becomes
  interesting, that is a different ADR with a safety section.
- **No second prompt-composition path.** See §1.
- **No abstraction beyond the two providers we have.** No plugin
  registry, no config-driven provider discovery.
- **No change to `load_skin_context`, the window, or the skin registry.**

## Consequences

**Positive.**
- Persona and window changes can be exercised before a key exists, on
  the real composition path.
- The question bank makes "does the persona work" answerable, and is
  reusable against Haiku unchanged.
- Contributors can run the app without a credential.
- The provider seam is where a third backend would go if one is ever
  wanted, without that being a reason to build one now.

**Negative.**
- A second code path is a second thing to keep working, and the one
  place it can rot — the provider boundary — is the one place tests
  can't reach without a live service. Mitigated by keeping the boundary
  narrow and shared above it.
- A local green run invites false confidence. The mitigation is social
  (the rule above) as much as technical, and social mitigations decay.
- Writing the question bank is real work for the course lead, and it is
  the part with no shortcut.

**Neutral.**
- One new dev-only dependency (an HTTP call to a local Ollama; no SDK).
- No schema, routing, or deployment change.

## Alternatives Considered

1. **Do nothing — iterate against Anthropic with a real key.** Honestly
   the strongest alternative: it tests the thing that actually ships, and
   at ~20¢ a run the cost objection is fake. Rejected only because the
   key isn't there yet and provisioning is the blocker in front of us —
   *not* because this approach is worse. If a dev key appears tomorrow,
   most of the value here evaporates and only the question bank (§3) and
   harness (§4) remain worth building. They are worth building either
   way, which is why they are the deliverable.
2. **Ollama behind an Anthropic-compatible proxy (LiteLLM or similar).**
   Zero changes to `claude_handler` — point `base_url` at the proxy.
   Rejected: trades a small amount of our code for a third-party process
   in the loop, another thing to run and version, and a translation layer
   that silently drops `cache_control` rather than us doing so knowingly.
3. **Record/replay fixtures — capture real Haiku responses once, replay
   them in tests.** Faithful and free after the first capture, and the
   right tool for *regression* ("did this refactor change the answer?").
   Useless for *exploration* ("does this new persona wording work?"),
   which is the current need. A complement, not a substitute; worth
   adding once a key exists and the bank has stabilised.
4. **Ship the persona untested and iterate on student reports.** What we
   are doing today by default. First-year students are a bad regression
   suite and a worse one to be wrong in front of.

### What the first throwaway run already turned up

Three questions against csc134/m0 through `llama3.2:3b`, using the real
composition path. At 3B nothing here transfers to Haiku — but one
finding does not depend on the model at all:

**The vendored corpus links to files we did not vendor.** Asked about a
due date, the bot correctly declined to invent one and then pointed at
`_tracking/course-manifest-csc134.yaml`. That path is real upstream and
absent from our corpus; `modules/m*/_assets.md` and `_overview.md`
reference `_tracking/skeleton-plan.md` and
`_tracking/numbering-reconciliation-map.md` the same way. A student
following that pointer finds nothing. Windowing created this: we vendor
a subset of a repo whose documents assume the whole repo. Either vendor
the referenced files, strip the links at sync, or tell the persona that
paths beginning `_tracking/` are not student-visible.

The two model-dependent observations, recorded as things for the bank to
watch rather than conclusions: the persona's "never hand over a
compilable solution" rule did not hold against a direct request even
with the full window loaded, and answers were not grounded in the
vendored walkthrough even when it was in context. Both are exactly what
a 3B is expected to do badly. Both are also exactly what the bank exists
to catch on Haiku, where they would matter.

## Open Questions

- **Who writes the question bank, and when?** It is the critical path
  and it is not an engineering task. Ten questions for `modules/m0`
  would be enough to start.
- **Which local model, and does the server have the memory for a useful
  one?** A 14B at 16k context is a real allocation on a box also serving
  a Flask app.
- **Does the harness run in CI?** It cannot call Anthropic on every PR
  without a budget, and a local model in CI is a second install to
  maintain. Probably manual to start, with the mechanical flags as the
  seed of a future gate.
- **How stale does a bank get?** It is written against a module's
  content; a corpus re-sync can invalidate its expectations silently.

## Follow-ups

- ADR-0004 (conditional): retrieval over the full corpus, if the
  one-module window proves too tight. (Carried over from ADR-0002's
  follow-ups, renumbered — this ADR took 0003.)
- Amend ADR-0002's window contract if `modules/mN` needs to be paired
  with `assignments/mN`. The first csc134 sync suggests it does.
