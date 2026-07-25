# M6 — Asset Slotting Notes

Records what slots into M6 and how, per the spine asset table
(`_storming/CSC-134-course-spine.md`, M6's "**Assets:**" line) and F-001
(`_lore/findings/F-001-numbering-reconciliation.md` /
`_tracking/numbering-reconciliation-map.md`). **Records intent only — nothing
is moved, renamed, or edited by this pass.**

Tags: **PORT** (adapt an existing asset) · **NEW** (author fresh) ·
**CONTRACT** (build against a frozen `_contracts/` file).

---

## Spine asset table, tagged

| Spine asset | Tag | Notes |
|---|---|---|
| *Chapter 3 — Functions: Breaking Down Problems Like a Pro Chef* | **PORT** | Learn-beat reading anchor. **Found on disk** at `_past_work/_claudes_input/02-functions-week3-4/chapter-03-functions.md` (285 lines) and its companion `chapter-04-parameters.md` (342 lines, parameters/pass-by-value-reference content). Uses a restaurant/chef-kitchen metaphor, not the course's dungeon/RPG theme — see reskin flag below. |
| *Module 02 — Functions* | **PORT** | **Found on disk** at `_past_work/_claudes_input/02-functions-week3-4/module-02-functions.md` (759 lines) and the folder's own `README.md` (123 lines). Structured as a 4-session, Week-3-4 unit with its own learning-objectives checklist, a "Restaurant Management System" capstone project, and an embedded "Flash" AI-assistant guide (`flash-guide.md`, 225 lines) — see AI-tooling flag below. |
| `_contracts/m5_menu.cpp` (canonical M5 menu program) | **CONTRACT** | The frozen file's own header comment states directly: "M6 refactors it into functions." Strong signal this is the intended canonical *input* for the Assess-beat refactor lab (see `_assess-spec.STUB.md`) — either as the class-provided starting shape, or as the reference a student's own M5 submission should structurally resemble. Not edited by this pass. |
| `_contracts/rubric-template.md` (four-column × four-tier rubric) | **CONTRACT** | Every M6 lab rubric (see `_assess-spec.STUB.md`) inherits this frozen interface. Do not fork it locally — file with the Spine Owner if it seems to not fit M6. |

**Exercise files found alongside the above** (not named directly in the spine's
Assets line, but living in the same ported folder and clearly M6-shaped —
flagged for deep-build to triage, not yet tagged PORT/NEW/drop):

| File | Contents |
|---|---|
| `_past_work/_claudes_input/02-functions-week3-4/exercises/debugging-02-functions.cpp` | A 6-bug debugging exercise (function-signature mismatches, missing `&`, etc.) — restaurant-order theme. |
| `_past_work/_claudes_input/02-functions-week3-4/exercises/practice-03-basic-functions.cpp` | Scaffolded void-function practice (restaurant greeting flow), prototypes partially blanked with TODO comments. |
| `_past_work/_claudes_input/02-functions-week3-4/exercises/practice-04-parameters.cpp` | Parameter-passing practice (177 lines) — not yet read in detail this pass. |
| `_past_work/_claudes_input/02-functions-week3-4/exercises/practice-05-scope.cpp` | Scope practice (201 lines) — not yet read in detail this pass; likely feeds MLO 6.1's "scope basics" clause and/or the Practice-beat exit ticket's "identify scope" item. |

---

## Legacy-content ledger (F-001)

Unlike M3 (whose legacy content sits under mis-numbered `assignments/m1`/`m2`),
**M6 has no legacy directory under `assignments/` at all** — `assignments/`
on disk currently holds only `m0/`, `m1/`, and `m2/`; there is no
`assignments/m6/` to record or reconcile. M6's pre-existing content lives
entirely under `_past_work/_claudes_input/02-functions-week3-4/` (see table
above), which is legacy-labeled but not spine-numbered at all (it is filed by
old chapter/module name, "02-functions-week3-4," not by any `m`-number).
Nothing in that folder was moved, renamed, or edited by this pass.

### Position-note reconciliation (already drafted, not yet applied)

`_tracking/numbering-reconciliation-map.md` (F-001) already drafts the exact
position-note insertions for two of these files — recorded here for
continuity, **not applied by this pass**:

- `_past_work/_claudes_input/02-functions-week3-4/module-02-functions.md`,
  line 1-2: proposed rewrite from `## Weeks 3-4 | Badge: Program Design and
  Implementation` to a version reading "Delivered as M6 (Weeks 9-10)" with an
  inserted position-note blockquote explaining the sequencing move (loops now
  precede functions).
- `_past_work/_claudes_input/02-functions-week3-4/chapter-03-functions.md`,
  line 1: proposed one-line position-note blockquote inserted directly below
  the existing title, same reconciliation reasoning.

Both edits remain **proposed, not executed** — F-001 renames/edits land later
with the owning module (this module, now that it's being scaffolded), per the
layout spec's non-clobber policy. This scaffold does not apply them.

### Caveat carried forward from F-001

The numbering-reconciliation-map itself flags uncertainty (its own open
question #4): `_past_work/` is self-declared archival, so it's possible the
spine's asset-table line "Chapter 3 / Module 02 — Functions" actually refers
to a not-yet-imported external working copy rather than this archived folder.
This folder is the only on-disk match for both "Chapter 3" and "Functions" by
title, so it's cited as the best available candidate, not a certainty —
deep-build should confirm before treating it as the final port source.

---

## Flags for deep-build (voice, tooling, tiering — not numbering)

1. **Theme mismatch.** The ported content uses a restaurant/chef-kitchen
   metaphor throughout (functions-as-kitchen-stations, a "Restaurant
   Management System" capstone). Per `CLAUDE.md`'s voice section, the course's
   canonical theme is dungeon/RPG, and "skin ≠ structure" means a theme must
   strip cleanly — so this is a **reskin decision for deep-build**, not a
   numbering issue: reskin to dungeon/RPG for consistency, or keep the
   restaurant skin as a demonstration that the structure survives a reskin.
   Either is defensible; recording the choice-point here so it's made on
   purpose.
2. **Embedded AI-tooling references.** `flash-guide.md` and sections of
   `module-02-functions.md` reference "Flash," an AI-assistant persona system
   apparently specific to the legacy course/platform this content was
   authored for. This is not the same as this course's own AI-permission
   ladder (see spine open question #4, "the AI-permission line per module").
   Deep-build should not port the Flash-persona framing as-is without
   reconciling it against this course's actual AI policy.
3. **`_contracts/m5_menu.cpp` as the refactor lab's starting artifact** is a
   confident recommendation, not an open question — the contract file states
   its own downstream use directly in its header comment. Flagging it clearly
   here so the `lab-creator` skill doesn't have to rediscover it.
4. **No numbering mismatch to flag for M6 itself** (unlike M3's ten
   mis-numbered legacy deliverables) — M6's port source was simply never filed
   under any `assignments/mN/` numbering, legacy or spine. The only pending
   F-001 item is the drafted-but-unapplied position-note text described above.
