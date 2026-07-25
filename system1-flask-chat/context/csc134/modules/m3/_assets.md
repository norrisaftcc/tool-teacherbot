# M3 — Asset Slotting Notes

Records what slots into M3 and how, per the spine asset table
(`_storming/CSC-134-course-spine.md`, M3's "**Assets:**" line) and F-001
(`_lore/findings/F-001-numbering-reconciliation.md` /
`_tracking/numbering-reconciliation-map.md`). **Records intent only — nothing
is moved, renamed, or edited by this pass.**

Tags: **PORT** (adapt an existing asset) · **NEW** (author fresh) ·
**CONTRACT** (build against a frozen `_contracts/` file).

---

## Spine asset table, tagged

| Spine asset | Tag | Notes |
|---|---|---|
| *Chapter 2 — Input, Processing, and Output* (`thinkcpp`) | **PORT** | Learn-beat reading anchor. Deep-build hasn't confirmed the source location on disk under this exact title yet — locate it via `_past_work/` or the Runestone `thinkcpp` reference before authoring. |
| *Pizza Calculator* rubric | **PORT** | Assess-beat anchor — the spine names it directly: "the Pizza Calculator project slots here." No file named "Pizza Calculator" turned up on disk during this scan. It likely lives inside the legacy `assignments/m1`/`m2` deliverables below (see ledger), or it hasn't been imported yet — the same status as M7's M6LAB2 per F-001. Flagging for deep-build to confirm the source before treating this as PORT vs NEW. |
| *Debugging Time — Fix These Broken Programs* | **PORT** | Supports the module's "debugging as curriculum" content beat (planned, celebrated first error). Not found on disk under this title during this scan — treat as not-yet-imported until deep-build locates or authors it. |
| `_contracts/rubric-template.md` (four-column × four-tier rubric) | **CONTRACT** | Every M3 lab rubric (see `_assess-spec.STUB.md`) inherits this frozen interface. Do not fork it locally — file with the Spine Owner if it seems to not fit M3. |

---

## Legacy-content ledger (F-001)

**The big one, per F-001 / the numbering-reconciliation map:** the course's
legacy `assignments/m1/` and `assignments/m2/` directories are numbered by the
*old* textbook-chapter order, not the spine's order. Their actual content —
variables, data types, `cin`/`cout`, arithmetic, formatted output — is spine
**M3 (Program Basics)** content, not spine M1 or M2. (Spine M1 and M2 are new,
not-yet-built modules: "Talk to Computers" and "How to Solve Problems.")

This ledger **records** that fact. It does **not** move, rename, or copy
anything — the legacy files stay exactly where they are, exactly as they are,
per the non-clobber policy.

| Legacy path | Legacy title | True spine home | Status |
|---|---|---|---|
| `assignments/m1/README.md` | "Module 1: Variables and Basic I/O" | **M3** | Frozen legacy — untouched |
| `assignments/m1/M1T1_HelloWorld.md` | "Your First Day as a Developer" (env setup + Hello World) | **M3** (possibly M0/M2 overlap — env-setup framing predates M3's variables scope; deep-build to confirm the exact split) | Frozen legacy — untouched |
| `assignments/m1/M1T2_DigitalBusinessCard.md` | "Digital Business Card" (variables, formatted output) | **M3** | Frozen legacy — untouched |
| `assignments/m1/M1LAB_CoffeeShopPOS.md` | "Coffee Shop POS System" (arithmetic, business logic) | **M3** | Frozen legacy — untouched |
| `assignments/m1/M1HW1_StudentBudgetAnalyzer.md` | "Student Budget Analyzer" (user input, calculations) | **M3** | Frozen legacy — untouched |
| `assignments/m2/README.md` | "Module 2: User Input and Advanced Calculations" | **M3** | Frozen legacy — untouched |
| `assignments/m2/M2T1_InteractiveMarketplace.md` | "Interactive Farmer's Market" (`cin`, prompts) | **M3** | Frozen legacy — untouched |
| `assignments/m2/M2T2_RestaurantCalculator.md` | "Restaurant Bill Calculator" (percentages, `iomanip`) | **M3** | Frozen legacy — untouched |
| `assignments/m2/M2LAB1_CrateManufacturing.md` | "Crate Manufacturing Analysis" (business calculations) | **M3** | Frozen legacy — untouched |
| `assignments/m2/M2HW1_MultiProgramChallenge.md` | "Multi-Program Challenge" (tiered: Bronze/Silver/Gold/Diamond) | **M3** | Frozen legacy — untouched |

Both legacy `README.md` files stay exactly as-is; this file (`_overview.md` in
this same directory) is the spine-truth overview and does not replace them.

### Pending reconciliation — do not resolve here

- **F-001 open question #7** (verbatim from `_tracking/numbering-reconciliation-map.md`
  §4): all ten of the above legacy deliverables map to spine M3. That's
  *heavier* than the spine's stated M3 scope (one small I/O + arithmetic
  program). Whether all ten survive as M3 artifacts, or some get trimmed or
  reassigned elsewhere, **needs an owner ruling before M3 is deep-built.**
  This scaffold does not make that call.
- **F-001 row 1 / row 6 naming drift:** legacy frontmatter and folder names use
  the zero-padded `M0X` / `M03` scheme (e.g., a `module: M03` field on
  external WIP — see below) where the spine uses bare `M3`. Renames land later
  with the owning module (this pass); flagged here, not fixed.
- **Actual port + renumber of `assignments/m1/*` and `assignments/m2/*` into
  this canonical `modules/m3/` tree is not done in this pass** — F-001 rename
  rows land with the owning module, per the layout spec's non-clobber policy.

---

## Adjacent WIP found during this scan (not touched, flagged for awareness)

`_storming/exemplars/m3-taco-receipt/` contains an M3-Assess-shaped exemplar
already in progress under a **different session's WIP**:
`M3LAB2_TacoReceipt.md`, `INSTRUCTOR_GUIDE.md`, `m3lab2_taco_c.cpp`,
`m3lab2_taco_a.cpp`. Its own frontmatter still reads `module: M03` (the exact
zero-padding drift F-001 row 1/6 names as a live bug in the skill-guild
templates). This asset:

- looks like a strong **PORT** candidate for the Assess beat (a "Taco
  Receipt" register program, tiered C/A, with a documented representation-vs-
  display payload — see the rounding trap noted in `_assess-spec.STUB.md`)
- was **not read for editing and not modified** — it belongs to another
  session per the numbering-reconciliation map's own caveat ("uncommitted WIP
  belonging to another session per my task brief")
- is recorded here only so deep-build knows it exists. Choose between the
  Pizza Calculator (spine-named) and the Taco Receipt (already-drafted) as
  M3's Assess anchor — or use both as an N-shot pair, the instructor guide's
  own framing

---

## Numbering flags for the Spine Owner

1. Legacy `assignments/m1/*` + `assignments/m2/*` are Program-Basics (spine
   M3) content living under spine-M1/M2 folder numbers. Recorded above per
   F-001; not renamed this pass.
2. `_storming/exemplars/m3-taco-receipt/M3LAB2_TacoReceipt.md` frontmatter
   carries `module: M03` (zero-padded) instead of bare `M3` — same bug class
   as F-001 row 5 (skill-guild templates). Not fixed this pass; flagged for
   whoever owns that WIP or the skill-template fix.
3. F-001 OQ7 (do all ten legacy M3-content deliverables survive, trimmed, or
   reassigned) is an open scope question blocking a confident Assess-beat
   pick between Pizza Calculator, Taco Receipt, and/or legacy deliverables.
   Needs an owner ruling before deep-build.
