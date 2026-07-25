# M5 — Asset Slotting Notes

Records what slots into M5 and how, per the spine asset table
(`_storming/CSC-134-course-spine.md`, M5's "**Assets:**" line) and F-001
(`_lore/findings/F-001-numbering-reconciliation.md` /
`_tracking/numbering-reconciliation-map.md`). **Records intent only — nothing
is moved, renamed, or edited by this pass.**

Tags: **PORT** (adapt an existing asset) · **NEW** (author fresh) ·
**CONTRACT** (build against a frozen `_contracts/` file).

---

## Spine asset table, tagged

| Spine asset | Tag | Notes |
|---|---|---|
| *Chapter 5* (`thinkcpp`) | **PORT** | Learn-beat reading anchor. Source location not yet confirmed on disk under this exact title — deep-build to locate via `_past_work/` or the Runestone `thinkcpp` reference before authoring, same open item M3 flagged for its Chapter 2. |
| *Module 04 — Loops (GameFAQs)* | **PORT** | Found on disk at `_past_work/_claudes_input/04-loops-week7-8/module04-loops-gamefaqs.md` (and a sibling variant `csc_134_m4_gamefaqs_guide.md` in the same folder — deep-build should confirm which is canonical or whether both merge). This single document already contains, internally, "Lab 7 — Loop Fundamentals," "Lab 8 — Professional Menu System," and "Project 2 Requirements" as sections (see ledger below) — it is not yet split into the separate Learn/Apply/Assess artifacts this scaffold's beat map calls for. |
| `M5LAB_A` (instructions, instructor guide, cheat sheet) | **PORT** | **Not found on disk as a standalone file under this name.** The spine and the learning-objectives doc both name `M5LAB`/`M5LAB_A` as the loop-fundamentals Assess anchor, but no file matching that name exists anywhere in this repo (confirmed via a repo-wide `find -iname "*M5*"`, which returns only `_contracts/m5_menu.cpp`). The nearest on-disk content is embedded inside the GameFAQs guide above (`[8.0] LAB 7 — LOOP FUNDAMENTALS`, `[9.0] LAB 8 — PROFESSIONAL MENU SYSTEM`). This is the same "named in spine, not yet extracted as its own file" status M3's Pizza Calculator carried — flagging for deep-build to confirm whether `M5LAB_A` is (a) this embedded section, ready to be lifted out, or (b) a genuinely separate not-yet-imported document. |
| **Loops Two-Skin Exemplar** | **PORT** | Found at `csc134-refresh-plan/04_loops_shared_exemplar.md` — a fully-drafted Learn-beat exemplar (turtle-square bridge -> Python/C++ "Level Up Stats" `for`-loop side-by-side -> PRIMM beat table). This is a strong, close-to-ready match for the spine's own M5 Learn line ("the turtle square as the iteration anchor") and the Apply beat's named "Level Up Stats" for-loop exercise. **Caveat per `CLAUDE.md`:** `csc134-refresh-plan/` is called out as a stale fork of the spine ("mine it for material, trust the spine"). The numbering-reconciliation map (row 9) confirms it has already drifted from canonical in at least one other spot (a stale "Precision" rubric-column name, superseded by ADR-002). Treat this file's *content* as a mining source, not as an authoritative, already-approved asset. Deep-build should re-verify it against the current spine before porting verbatim. |
| `_contracts/m5_menu.cpp` (canonical M5 menu program) | **CONTRACT** | The frozen interface every M5 Apply/Assess artifact builds against — the M4 gatekeeper wrapped in a validated `do/while` menu loop (the M4->M5 seam, per its own header comment). Read-referenced by `_overview.md` and `_assess-spec.STUB.md`; not edited. Compiles clean per `_contracts/README.md`'s own verification note. If this contract seems to not fit M5's needs, file the finding with the Spine Owner — do not fork it locally. |
| `_contracts/rubric-template.md` (four-column x four-tier rubric) | **CONTRACT** | Every M5 lab rubric (see `_assess-spec.STUB.md`) inherits this frozen interface. Do not fork it locally — file with the Spine Owner if it seems to not fit M5. |

---

## Legacy-content ledger (F-001)

Unlike M3 (whose legacy content sits under misnumbered `assignments/m1/` and
`assignments/m2/` folders), **M5's legacy content is already correctly
numbered** per F-001 / the numbering-reconciliation map's own row 1 finding:
`M5LAB` (loops) resolves as correctly M5, and the folder
`_past_work/_claudes_input/04-loops-week7-8/` already sits where it should —
no rename is owed here. This ledger records what that folder actually
contains and its true spine home for completeness, not to flag a numbering
problem.

| Legacy path | Legacy title | True spine home | Status |
|---|---|---|---|
| `_past_work/_claudes_input/04-loops-week7-8/README.md` | "Module 04: Loops - The Boss Battle Against Repetition" | **M5** | Frozen legacy — untouched |
| `_past_work/_claudes_input/04-loops-week7-8/module04-loops-gamefaqs.md` | Primary loop GameFAQs tutorial (While/Do-While/For/Validation/Nested/Menu Pattern + Lab 7 + Lab 8 + Project 2 + rubric + bug guide) | **M5** | Frozen legacy — untouched |
| `_past_work/_claudes_input/04-loops-week7-8/csc_134_m4_gamefaqs_guide.md` | Alternative-version loop GameFAQs guide (sibling to the above; deep-build to confirm which is canonical or whether they merge) | **M5** | Frozen legacy — untouched |
| `_past_work/_claudes_input/04-loops-week7-8/m4_faq.md` | Supplemental FAQ (loops) | **M5** | Frozen legacy — untouched |
| `_past_work/_claudes_input/04-loops-week7-8/m4_supplemental.md` | Supplemental material (loops) | **M5** | Frozen legacy — untouched |
| `_past_work/_claudes_input/04-loops-week7-8/m4_test_log.txt` | Instructor test log | **M5** (instructor-facing only — do not surface to students per the dungeon-canon/build-org-meta separation) | Frozen legacy — untouched |
| `csc134-refresh-plan/04_loops_shared_exemplar.md` | "Loops — The Two-Skin Exemplar (Phase D)" | **M5** | Frozen legacy (stale-fork tree, per `CLAUDE.md`) — untouched |

`assignments/m5/` does not currently exist on disk (confirmed — no such
directory in this repo). There is no legacy `assignments/m5/*` content to
record for this module; unlike M3, M5 has no misnumbered-folder problem to
carry forward. **Per the layout spec's non-clobber policy, `assignments/`
remains frozen and is not a scaffold target regardless — this canonical
`modules/m5/` tree is the only spine-truth home going forward.**

### Pending reconciliation — do not resolve here

- **`M5LAB_A` has no physical file of its own** — its content appears to live
  embedded inside `module04-loops-gamefaqs.md`'s Lab 7/Lab 8/Project 2
  sections. Whether deep-build extracts these into a standalone
  `M5LAB_A`-named file (matching the spine's own naming) or authors fresh
  against the embedded content as a reference is an open call, not resolved
  by this scaffold.
- **Two candidate GameFAQs guides exist side by side**
  (`module04-loops-gamefaqs.md` and `csc_134_m4_gamefaqs_guide.md`) with no
  on-disk note explaining which is canonical, if either. Flagged for
  deep-build, not resolved here.
- **The Loops Two-Skin Exemplar's turtle-square material lives in the
  stale-fork `csc134-refresh-plan/` tree**, not in `_past_work/` or
  `_storming/`. Mining it is fine per `CLAUDE.md`. Treating it as
  already-approved canon is not — deep-build should re-verify its content
  (especially any rubric-column or terminology references) against the
  current spine and ADR-002/ADR-004 before porting verbatim.
- **No numbering mismatch found for M5 itself** (contrast with M3): F-001
  row 1 already ruled `M5LAB` / `04-loops-week7-8` correctly numbered.
  Nothing here needs a Spine Owner rename ruling the way M3's
  `assignments/m1`+`m2` content does.

---

## Numbering flags for the Spine Owner

1. **No numbering mismatch to flag for M5's own legacy folder** — F-001 row 1
   already confirms `04-loops-week7-8` / `M5LAB` is correctly positioned.
2. **`M5LAB_A` is named in the spine and learning-objectives doc but has no
   matching physical file** — same "referenced, not yet extracted" status as
   M3's Pizza Calculator (F-001 open question #7 territory, though this is a
   missing-file finding rather than a scope-trim question). Recorded here for
   deep-build, not as an F-001 numbering item — no rename is at stake. This
   just confirms a discoverability gap for whoever deep-builds M5.
3. **`csc134-refresh-plan/04_loops_shared_exemplar.md`** is a strong content
   match for M5's Learn/Apply beats but lives in the stale-fork tree
   `CLAUDE.md` warns builders to treat as non-authoritative. Flagging so a
   future ruling can decide whether this file (or its content) should be
   formally ported into `_past_work/` or `_storming/` as a non-stale source,
   rather than staying in the fork tree indefinitely.
