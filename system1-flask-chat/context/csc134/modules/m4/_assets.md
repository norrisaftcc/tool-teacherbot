# M4 — Asset Slotting Notes

Records what slots into M4 and how, per the spine asset table
(`_storming/CSC-134-course-spine.md`, M4's "**Assets:**" line) and F-001
(`_lore/findings/F-001-numbering-reconciliation.md` /
`_tracking/numbering-reconciliation-map.md`). **Records intent only — nothing
is moved, renamed, or edited by this pass.**

Tags: **PORT** (adapt an existing asset) · **NEW** (author fresh) ·
**CONTRACT** (build against a frozen `_contracts/` file).

---

## Spine asset table, tagged

| Spine asset | Tag | Notes |
|---|---|---|
| *Chapter 4 — Decision Structures: Build Your Own Adventure* | **PORT** | Learn-beat reading anchor. The spine's own asset table (`CSC-134-course-spine.md:362`) names this "Chapter 4 / Module 03" together as one entry. On disk, the two show up as *separate* documents (see ledger below), not one merged chapter. Deep-build should confirm whether they merge into a single Learn reading, or split across Learn (chapter prose) and Apply/Assess (the project spec). |
| *Module 03 — Decision Structures* | **PORT** | Same spine asset-table row as above. On disk, this is the GameFAQs-styled guide (`module03-gamefaqs-guide.md`) and its Canvas-formal sibling (`module03-canvas-assignment.md`) — see ledger. Per F-001 row 11, the folder name `03-decisions-week5-6` and its README's own header ("Module 03: Decision Structures") are **already correctly reconciled to M4**. No rename is owed here, unlike M3's legacy folders. |
| `_contracts/m4_gatekeeper.cpp` (canonical M4 decision program) | **CONTRACT** | The frozen interface every M4 Apply/Assess artifact builds against — the Dungeon Gatekeeper: `switch` on character class, `if`/`else if`/`else` on a strength threshold, one compound condition (`&&`) gating a Rogue's lockpick shortcut, no loops, no functions (pre-M6 single-file form). Its own header comment names it as the seam anchor for `_contracts/m5_menu.cpp`, which wraps this same decision core in a `do/while` loop. `_overview.md` and `_assess-spec.STUB.md` read-reference this file but don't edit it. Compiles clean per `_contracts/README.md`'s own verification note. If this contract seems to not fit M4's needs, file the finding with the Spine Owner. Do not fork it locally. |
| `_contracts/rubric-template.md` (four-column x four-tier rubric) | **CONTRACT** | Every M4 lab rubric (see `_assess-spec.STUB.md`) inherits this frozen interface: four columns — Correctness, Completeness, Format, Submission. Correctness is locked as column one per ADR-002 (never "Precision"). Do not fork it locally. File with the Spine Owner if it seems to not fit M4. |

---

## Legacy-content ledger (F-001)

Like M5 (and unlike M3), **M4's legacy content is already correctly
numbered**, per F-001 row 11 / the numbering-reconciliation map. The
`_past_work/_claudes_input/03-decisions-week5-6/` folder's own README header
("Module 03: Decision Structures," weeks 5–6) already matches spine M4.
No rename is owed here. Unlike M5, there is also **no `assignments/m4/`
directory at all**. `assignments/` on disk holds only `m0`, `m1`, and `m2`
(confirmed via directory listing), so there is no drifted-folder problem to
carry forward from that tree either. This ledger records what the
`_past_work/` folder actually contains and its true spine home for
completeness, not to flag a numbering problem.

| Legacy path | Legacy title | True spine home | Status |
|---|---|---|---|
| `_past_work/_claudes_input/03-decisions-week5-6/README.md` | "Module 03: Decision Structures - Your Code Learns to Think" (dual-flavor index pointing at the two files below) | **M4** | Frozen legacy — untouched |
| `_past_work/_claudes_input/03-decisions-week5-6/module03-canvas-assignment.md` | "Module 03: Decision Structures in C++ Programming" — Canvas-formal version (100-pt Project 1 rubric, traditional structure) | **M4** | Frozen legacy — untouched |
| `_past_work/_claudes_input/03-decisions-week5-6/module03-gamefaqs-guide.md` | GameFAQs-styled guide — same concepts, retro-ASCII/gaming framing, "boss battle" language for nested `if`s | **M4** | Frozen legacy — untouched |
| `_past_work/_claudes_input/03-decisions-week5-6/03_overview_agents_md.html` | Rendered/exported HTML copy of an overview doc (unconfirmed exact source relationship to the two files above) | **M4** | Frozen legacy — untouched; deep-build to confirm whether this is a stale export or carries independent content |

`assignments/m4/` does not currently exist on disk (confirmed — no such
directory in this repo). `assignments/` holds only `m0`, `m1`, `m2`. There is
no legacy `assignments/m4/*` content to record for this module. **Per the
layout spec's non-clobber policy, `assignments/` remains frozen and is not a
scaffold target regardless. This canonical `modules/m4/` tree is the only
spine-truth home going forward.**

### Pending reconciliation — do not resolve here

- **Two full prior-offering variants exist side by side:**
  `module03-canvas-assignment.md` and `module03-gamefaqs-guide.md`. Each
  covers the same learning objectives in a different voice and format. A
  README frames them as student-selectable "flavors." The spine's LPAA
  map does not ask students to choose a format. It specifies one Learn
  reading, one Apply tutorial, one Assess lab. Deep-build must decide whether
  to mine one as primary and the other as a style reference, or merge both.
  This scaffold does not resolve it.
- **The `03_overview_agents_md.html` file's relationship to the two Markdown
  guides is unconfirmed.** It may be a stale rendered export of one of them,
  or an independent document. Flagged for deep-build, not resolved here.
- **Instructor-only material check.** Unlike M5's legacy folder (which
  carries an explicit `m4_test_log.txt` instructor-only file), nothing in
  `03-decisions-week5-6/` is self-labeled instructor-only on a first pass.
  But the GameFAQs guide's "Pro Tips from Previous Students" and Flash-AI
  persona framing (Flash-Creative/Flash-Debug/Flash-Organizer) are
  build-era course branding, not this spine's AI-use convention. Deep-build
  must strip or re-skin any such build-org meta before it reaches students.
  That follows the dungeon-canon/instructor-facing-only rule.
- **The Dungeon Gatekeeper theme vs. the legacy "Choose Your Own Adventure"
  theme.** `_contracts/m4_gatekeeper.cpp` frames M4's canonical program as a
  dungeon gate scene. The legacy `_past_work/` guides frame the same
  objectives as an open-genre "text adventure" — sci-fi, mystery, survival,
  etc. are all offered as reskins. Both are theme-compatible with the
  spine's CYOA Assess line. Deep-build should decide whether the gatekeeper
  contract's theme becomes the required Assess skin, or stays one option
  among the legacy guide's reskins. Either way, the course convention holds:
  a lab's theme must be freely re-skinnable without breaking the exercise.

---

## Numbering flags for the Spine Owner

1. **No numbering mismatch to flag for M4's own legacy folder.** F-001
   row 11 already confirms `03-decisions-week5-6` is correctly positioned
   against spine M4 (README title "Module 03: Decision Structures" ==
   spine's own asset-table entry "Chapter 4 / Module 03 — Decision
   Structures"). Nothing here needs a Spine Owner rename ruling.
2. **No `assignments/m4/` directory exists**, so there is no drifted-folder
   problem analogous to M3's `assignments/m1`+`m2` situation. Only the
   `_past_work/` folder above is in scope for this module's porting work.
3. **Two candidate primary documents exist side by side** — Canvas-formal vs.
   GameFAQs — with no on-disk note ruling one canonical. This is the same
   "pick-one-or-merge" shape M5 flagged for its two GameFAQs guides.
   Flagged for deep-build, not resolved here.
