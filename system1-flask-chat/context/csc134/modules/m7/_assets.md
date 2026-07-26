# M7 — Asset Slotting Notes

Records what slots into M7 and how, per the spine asset table
(`_storming/CSC-134-course-spine.md`, M7's "**Assets:**" line) and F-001
(`_lore/findings/F-001-numbering-reconciliation.md` /
`_tracking/numbering-reconciliation-map.md`). **Records intent only —
nothing is moved, renamed, or edited by this pass.**

Tags: **PORT** (adapt an existing asset) · **NEW** (author fresh) ·
**CONTRACT** (build against a frozen `_contracts/` file).

---

## Spine asset table, tagged

| Spine asset | Tag | Notes |
|---|---|---|
| `M6LAB2` (parallel arrays → `Room` struct array) | **PORT** | Feeds the C-tier of `M7LAB1` directly (spine's C-tier line is verbatim M6LAB2's job: "refactor parallel arrays into a Room struct array"). **Confirmed not a physical file anywhere in this repo** (no `find` hit for `M6LAB2`/`M6LAB*` under any extension during this scan) — matches the numbering-reconciliation map's own finding. Not-yet-imported; deep-build must locate the source material or author it fresh, and resolve whether it lands as a standalone ported file or is absorbed as `M7LAB1`'s C-tier section outright (see "Pending reconciliation" below — this is F-001's open question #1, unresolved). |
| `M7LAB1` (structs, tiered: Room → Hero → Monster → class) | **PORT** | The Assess-beat anchor itself; spine names it directly. **Confirmed not a physical file anywhere in this repo** during this scan — same not-yet-imported status as `M6LAB2`. Deep-build via the `lab-creator` skill against `_assess-spec.STUB.md`'s acceptance-criteria skeleton, using whatever source material can be located, or authoring fresh against the spine's own tier description if no source is found. |
| *Terminal Graphics for Codespaces and Windows* (richer output companion) | **PORT** | Spine's own framing: "richer output belongs here" — i.e., pairs with M7's struct/class work to give students nicer console presentation for their `Room`/`Hero`/`Monster` data. Not found on disk under this title during this scan — treat as not-yet-imported, same status as the two labs above. |
| *So Your Turtle Code Became Spaghetti* (refactoring-mindset companion) | **PORT** | A refactoring-mindset reading, pairs naturally with the struct-refactor arc (parallel arrays → struct is itself "spaghetti becomes clean" in miniature). Not found on disk under this title during this scan — not-yet-imported. |
| `_contracts/rubric-template.md` (four-column × four-tier rubric) | **CONTRACT** | Every M7 lab rubric (see `_assess-spec.STUB.md`) inherits this frozen interface. Do not fork it locally — file with the Spine Owner if it seems to not fit M7. |
| `_contracts/m5_menu.cpp` (canonical M5 menu program) | **CONTRACT** | Not an M7-named asset in the spine's own table, but flagged here because the spine states elsewhere that "M7 extends it" (the M4→M5→M6→M7 program lineage: gatekeeper → menu → functions-refactor → structured-data-extension). Deep-build should confirm whether M7's Apply-beat "here's 80%" starting program is meant to be a direct descendant of this contract file, or an independent `Room`/`Hero` build — the spine's M7 section itself does not name `m5_menu.cpp` explicitly, so this is a plausible-but-unconfirmed lineage, not a locked requirement. |

---

## Legacy-content ledger (F-001)

**Unlike M3, M7 has no legacy `assignments/mN/` folder collision to record.**
As of this scan, `assignments/` contains only `m0/`, `m1/`, and `m2/` — there
is no `assignments/m7/` (nor an `assignments/m6/`) holding drifted content
under this module's own number. This module's asset problem is not
"content sitting under the wrong folder number" (M3's problem); it is
"named source assets that do not yet exist as physical files anywhere in
this repo" — confirmed by direct search (`find . -iname "*M6LAB2*" -o -iname
"*M7LAB1*"` and separate searches for "terminal graphic" and "turtle"/
"spaghetti" all returned zero hits).

| Named asset | Expected legacy home (if any) | Status |
|---|---|---|
| `M6LAB2` | None found — not `_past_work/`, not `assignments/`, not `_storming/exemplars/` | Not-yet-imported (F-001) |
| `M7LAB1` | None found | Not-yet-imported (F-001) |
| *Terminal Graphics for Codespaces and Windows* | None found | Not-yet-imported (F-001) |
| *So Your Turtle Code Became Spaghetti* | None found | Not-yet-imported (F-001) |

This ledger **records** the absence. It does not author replacement content,
and it does not search outside this repository (e.g., an instructor's local
drive or an LMS) — that search, if needed, is a deep-build task.

### Pending reconciliation — do not resolve here

- **F-001 open question #1** (verbatim from
  `_tracking/numbering-reconciliation-map.md` §4): does `M6LAB2` land as a
  standalone ported file (e.g., `M7LAB0_ParallelArraysToStruct`) under M7, or
  get absorbed as `M7LAB1`'s C-tier section outright? The spine's own Assess
  line describes `M7LAB1`'s C-tier in exactly `M6LAB2`'s terms, which is why
  `_assess-spec.STUB.md` in this folder writes the C-tier as if it is already
  absorbed. But the reconciliation map flags this as still open, pending a
  builder/maintainer call. **RESOLVED (2026-07-24, Q3 ruling):** neither absorb
  nor standalone-lab — `M6LAB2`'s parallel-arrays→`Room`-struct-array move
  becomes **M7's Apply-beat exemplar** (the spine already calls for an M7 Apply
  that "builds a `Room` struct array"; the transformation *is* that hands-on
  beat). `M7LAB1` remains the **Assess** anchor and grades the result — Apply
  teaches the move, Assess tests it, one contract artifact. Deep-build authors
  the Apply against this; the `_assess-spec.STUB.md` C-tier stays as the Assess's
  own tier, no longer doubling as the stepping-stone. Lightweight packaging call
  within the ratified Room/Hero contract — recorded here, no ADR.
- **F-001 open question #2:** the legacy course manifest's `M06`
  (Arrays/Strings/STL) and `M07` (File I/O/Structs) entries partially overlap
  M7's scope (the struct half of manifest-`M07` clearly maps here) but also
  carry STL/`std::string` and File I/O content that **has no home anywhere in
  the current spine** — absent from M7's own section and from the CCL
  crosswalk. This is a scope ruling (likely its own ADR), not something this
  numbering pass or this scaffold resolves. Flagged here because it directly
  bears on M7's `_assets.md` per the layout spec's own instruction.
- **Manifest `M08` (Introduction to OOP)** also splits across two spine
  modules per the reconciliation map: its classes/OOP half belongs to M7
  (the struct→class arc), while its capstone-shaped deliverables
  (`project-oop-rpg`, `capstone-portfolio`) belong to M8. Deep-build should
  confirm no OOP-relevant legacy manifest content is silently dropped when
  M7's Learn/Apply/Assess beats are authored.

---

## Numbering flags for the Spine Owner

1. **Task-instruction / layout-spec conflict, surfaced during this build**
   (not a numbering issue per se, but adjacent — recorded here since it
   affects where this ledger and its siblings live). This scaffold pass was
   instructed to "Scaffold `assignments/m7/`," but the authoritative layout
   spec states plainly that canonical scaffolds land in `modules/mN/`, and
   that "legacy `assignments/` is frozen and never a scaffold target." The
   precedent already on disk (`modules/m0/`, `m1/`, `m2/`, `m3/` — each built
   the same way, each with its own `_overview.md` stating "`assignments/` is
   legacy source... frozen, not a scaffold target") confirms the layout spec
   is load-bearing, not the shorthand instruction. **This pass built
   `modules/m7/`, matching the existing canonical tree and the layout spec,
   and did not create or touch any `assignments/m7/` path.** Flagging this
   explicitly so the Spine Owner can correct the instruction template if the
   mismatch recurs for future modules.
2. All four of M7's named spine assets (`M6LAB2`, `M7LAB1`, *Terminal
   Graphics*, *Turtle→Spaghetti*) are confirmed not-yet-imported — zero
   physical files found under any of the four names or close variants,
   anywhere in this repository, as of this scan. This matches
   `_tracking/numbering-reconciliation-map.md` row 2/3's own finding for the
   first two labs and extends the same confirmation to the two companion
   readings, which the reconciliation map did not check.
3. F-001 open question #1 (M6LAB2's landing shape) directly shapes this
   module's Assess-spec stub, as noted above — needs an owner ruling before
   `_assess-spec.STUB.md` is instantiated into a real lab.
4. F-001 open question #2 (STL/`std::string` and File I/O's missing spine
   home) touches M7 because both legacy manifest entries partially overlap
   its Arrays/Structs scope — needs a scope ruling, not a numbering fix,
   before deep-build finalizes M7's boundaries.
