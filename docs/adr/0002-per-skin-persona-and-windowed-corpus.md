# ADR-0002: Per-skin persona, and window the corpus to one module

- **Status:** Proposed
- **Date:** 2026-07-25
- **Deciders:** norrisaftcc (product), Claude Code (implementation)

## Context

ADR-0001 made the cohort a *skin*: per-skin URL prefix, passcode, model,
cohort header, and vendored corpus. It deliberately left two things
shared, and both are now biting.

**1. The persona is still hardcoded, and it is the wrong one.**
`claude_handler.build_system_prompt` opens with:

> You are an AI teaching assistant for the AlgoCratic Futures capstone course.

…followed by the Sacred Workflow rule and the AlgoCratic vocabulary
substitutions ("growth opportunity" not "error", "The Algorithm
suggests" not "You should"). Every skin gets that text. CSC 134 is an
introductory **C++** course — Codespaces, `cout`, `cin`, functions,
arrays — with students meeting programming for the first time. Telling
them The Algorithm suggests a suboptimal pointer is noise at best.
ADR-0001 listed this divergence as a conditional follow-up; the CSC 134
launch makes it unconditional.

**2. `load_skin_context` loads the entire corpus into every request.**
It `rglob('*.md')`s the whole corpus directory and concatenates the
result into the system prompt. There is no caching, so the full corpus
is re-sent and re-billed on every single message.

| Corpus | On disk (md) | Per message |
|---|---|---|
| csc114 today (crosswalk + 2 weeks) | 83 KB | ~21k tokens |
| csc134 upstream, everything | 424 KB | ~106k tokens |

The csc134 manifest on main assumes a `planning/pilot_su26/` layout that
does not exist upstream; the real
`norrisaftcc/course-csc134-template` is `outline/` (9 KB) plus
`modules/m0…m8` (17–34 KB each, except m4 at 115 KB) plus
`assignments/m0…m2` and an `instructor-guide/`. Syncing it as-is would
put a six-figure token count in front of Haiku on every turn *and* ship
the instructor guide to students.

The operating insight from the course lead: a student in week 3 does not
need modules 4 through 8 in context. **Base persona plus the current
module is all that should ever be in memory.**

Trusted-workflow constraints: Issue → ADR → PR, one substantive change
per PR, no unrelated cleanup.

## Decision

Make the system prompt a composition of three per-skin parts, and window
the corpus to a single module.

```
system prompt = persona (per-skin file)
              + cohort header (per-skin file)
              + corpus index (small, always on)
              + active module only (windowed)
```

1. **Persona becomes a per-skin markdown file.** `Skin` grows
   `persona_file`, resolved under `context/` exactly like `header_file`:

   - `context/csc114_persona.md` — the current AlgoCratic capstone text,
     **moved verbatim**. CSC 114 is a live cohort mid-pilot; this change
     must not alter a single token of what those students already see.
   - `context/csc134_persona.md` — new. Intro-C++ TA: plain voice, no
     AlgoCratic seasoning, short concrete answers, never hands over a
     compilable solution, asks for the student's attempt and the actual
     compiler error first, teaches the fork → branch → commit → PR loop
     the course already uses in Codespaces.

   `auth.load_skin_persona(slug)` reads it. Prose lives in markdown so an
   instructor can retune the voice without touching Python.

2. **`claude_handler` takes the persona as data.**
   `build_system_prompt(course_context, persona=None)` composes
   persona + context; `get_claude_response` / `stream_claude_response`
   gain a `persona=` keyword. A module-level `DEFAULT_PERSONA` — a
   neutral, course-agnostic TA persona with the pedagogical guardrails
   but no AlgoCratic vocabulary — is the fallback when a caller omits
   it, mirroring how `MODEL` already degrades. The fallback is a safety
   net for library callers, not a route path: routes always pass one.

3. **`load_skin_context` windows to the active module.** `Skin` grows:

   - `corpus_index: list[str]` — small always-on files relative to the
     corpus dir (`crosswalk.md`, `outline/`). Orientation material; the
     bot needs to know what exists.
   - `active_module: str | None` — one subdirectory of the corpus dir.
     Only its `.md` files are loaded. `None` means load nothing beyond
     the index.

   Everything outside index + active module stays on disk, vendored and
   ready, but out of the prompt. The symlink-escape guards from ADR-0001's
   implementation are preserved as-is.

4. **The active module is bumpable without a deploy.** An env var
   `<SLUG>_ACTIVE_MODULE` (e.g. `CSC134_ACTIVE_MODULE=m3`) overrides the
   registry value. Weekly advance becomes a Render env edit and a
   restart, not a code push. An override naming a directory that does not
   exist falls back to the registry value and logs — a typo in the Render
   dashboard must not empty the bot's context silently.

5. **The csc134 manifest is corrected to the real upstream layout** —
   `outline/`, `modules/`, `assignments/` — and the `instructor-guide/`
   is explicitly **not** vendored. Student-facing bot; instructor
   materials do not belong in it.

6. **Cache the module.** Windowing makes the system prompt byte-stable
   for every student in a cohort on a given module, which is exactly the
   shape prompt caching wants. The system prompt ships as a single
   cached block — `cache_control: {"type": "ephemeral", "ttl": "1h"}` —
   so the second and every later message in a class period bills the
   corpus at ~10% of input price instead of full freight.

   The 1-hour TTL rather than the 5-minute default is deliberate: usage
   is bursty around class periods, and a 1-hour entry survives a student
   thinking for ten minutes between questions. It costs 2× on the write
   (vs. 1.25× at 5 minutes), so it pays back from the third read on —
   trivially met by a cohort sharing one module window.

   Caching is *enabled by* the window, not a substitute for it: the
   cached block is the same block for the whole cohort, so one write
   serves every student. Note the floor — **Haiku 4.5 will not cache a
   prefix under 4096 tokens**, silently, with no error. A skin with a
   header and no corpus falls under that floor; the module window keeps
   csc134 comfortably above it.

Resulting per-message context: csc114 ≈ crosswalk + one week ≈ 58 KB
(down from 83 KB); csc134 ≈ outline + one module ≈ 26–43 KB (down from
424 KB), with m4 the outlier the course lead may want to split. On top
of that, cache hits bill the block at ~10%.

### What we deliberately do not change

- **UI chrome.** `templates/` still says "AlgoCratic TA" and "The
  Algorithm is watching" for both skins. Visible, but it is a template
  pass, not a prompt-composition change. Follow-up.
- **Retrieval.** No tool-use, no file-browsing agent, no embedding index.
  A static one-module window is dead simple and covers the actual need.
  Revisit only if students demonstrably ask cross-module questions.
- Database schema, routing contract, design kit — untouched.

## Consequences

**Positive.**
- CSC 134 students get a persona that matches their course. CSC 114
  students see no change at all.
- Per-message context drops ~10x for csc134 and ~30% for csc114. Haiku
  on a 30 KB prompt is a viable per-student cost profile; Haiku on a
  424 KB prompt is not.
- Persona and window are both data. Retuning voice is a markdown edit;
  advancing a week is an env var.
- The corpus can be vendored in full — the sync script no longer has to
  double as a curation tool.

**Negative.**
- Someone must remember to advance `active_module` each week. Mitigated
  by the env override, not eliminated. A stale pointer means the bot is
  a week behind, which is quiet rather than loud.
- A student asking about last week's material gets a bot that cannot see
  it. Acceptable for v1; the cohort header names the course shape, and
  the index keeps the outline in view so the bot can say "that was
  module 2" rather than hallucinate.
- Two more per-skin files to keep in sync when a cohort is added. The
  registry entry now has eight fields.
- Every edit to a persona file, cohort header, or the active module
  invalidates that skin's cache — the next message pays one cold write.
  Cheap and self-healing, but it means retuning a persona mid-class has
  a (small) cost, and it is a reason not to put anything per-request
  into the system prompt.

**Neutral.**
- No new dependencies. No schema change. Test count grows.

## Alternatives Considered

1. **Persona strings inline in the `SKINS` dict.** No new files, but
   multi-line prose in a Python literal is miserable to edit and invites
   escaping bugs. Rejected — `header_file` already set the file-path
   precedent.
2. **Fold the persona into the existing `<slug>_context.md` header.**
   Smallest possible diff. Rejected: the header is cohort *facts* and is
   hand-maintained next to vendored corpus, while the persona is
   *behavior* and wants to be reviewed as such. Conflating them makes it
   easy to break guardrails while editing a cohort description.
3. **Curate at sync time — vendor only the current module.** Keeps the
   loader as-is; advancing a week means re-running the sync script and
   committing a corpus churn diff every week. Rejected: git noise, and
   it couples "what is on disk" to "what is in context".
4. **Retrieval over the full corpus (tool-use or embeddings).** Best
   answer quality ceiling, far more machinery, and a whole new failure
   surface for a bot that must be reliable in front of first-time
   programmers. Rejected for v1 (see Follow-ups).
5. **Prompt caching instead of windowing.** Cuts cost without cutting
   tokens, but a 106k-token prompt still degrades a Haiku answer with
   material the student will not touch for two months. Cost was not the
   only problem. Do both, in that order.

## Open Questions

- **CSC 114's active module.** The registry needs a value now. The
  implementation PR sets `week-02-keras-hello-world` (the latest week
  vendored) with `crosswalk.md` as index. Course lead confirms or bumps.
- **CSC 114's voice.** The AlgoCratic text moves verbatim on the
  principle of not changing a live cohort mid-pilot. Whether CSC 114
  *should* still be AlgoCratic-flavored is a product call, and now a
  one-file edit either way.
- **Module m4 (115 KB).** Four to six times its siblings. Split
  upstream, or accept one heavy week.
- **Assignments alongside modules.** Vendored, but not in the window —
  `assignments/mN/` does not sit under `modules/mN/`. Either the index
  grows a per-module assignment path or `active_module` becomes a list
  of globs. Deferred until the first week where it actually bites.

## Follow-ups

- ADR-0003 (conditional): retrieval over the full corpus, if the
  one-module window proves too tight.
- Template pass: retire AlgoCratic UI chrome, or make it per-skin.
