# M2 — Asset slotting + legacy ledger

> **SKELETON.** Records intent and provenance; reconciles nothing. No files
> are moved, renamed, or deleted by this pass (F-001 renames land later, with
> their owning module).

## Asset table (from spine's M2 section + module-identity map)

| Asset | Tag | Notes |
|---|---|---|
| Runestone `thinkcpp` reading checkpoints | **PORT** | Spine: "reading checkpoints; functions coverage lands in Ch. 3, matching our functions module." Adapt the relevant `thinkcpp` chapter/checkpoint for the Learn beat's Predict-the-output anchor. External resource — port the checkpoint framing, not a file in this repo. |
| Communication decks | **PORT** | Spine lists these as an M2 asset alongside `thinkcpp`. Likely overlaps with the Robot-Sandwich explainer decks named as M1's asset (`_storming` M1 section, ~line 132) — deep-build should confirm whether "Communication decks" here is the same deck reused, or a distinct M2-specific deck, before assuming duplication. |
| Hello World tour (HTML/CSS → JS → Python → C++ → assembly slice) | **NEW** | No existing asset found on disk. Authored fresh for the Learn beat. |
| Four-word error taxonomy table (Syntax / Static semantic / Runtime / Logic) | **NEW** | Content itself is fixed course-wide (see `CLAUDE.md` mechanical bar #4 and the spine table at ~line 142), but the M2 teaching materials that *introduce* it are new authorship. |
| Flowcharts (Mermaid) / pseudocode / user-story ("As a ___...") teaching material | **NEW** | No existing M2-specific asset found; author fresh. Mermaid tooling itself is shared infra (per `CLAUDE.md`: "reuses the M1 skill"), not a new asset. |
| "Perspective Flip" Assess pattern (read a working program, describe it, draw its flowchart) | **NEW** | Named in spine as "our version of CTI's Perspective Flip" — no CSC-134-side asset exists yet; author fresh, informed by CTI's version if/when available for reference (not a port target since it's CTI's sibling course, not this repo). |
| `_contracts/rubric-template.md` | **CONTRACT** | The Assess-beat rubric (`_assess-spec.STUB.md` in this folder) inherits its four columns (Correctness/Completeness/Format/Submission) and tier ladder verbatim in shape. Frozen interface — do not fork. |

No `_contracts/*.cpp` program contract applies to M2 (those are M4's
`m4_gatekeeper.cpp` and M5's `m5_menu.cpp` — both later modules).

---

## Legacy-content ledger — `assignments/m2/` (READ THIS BEFORE ASSUMING A MATCH)

**`assignments/m2/` on disk does NOT hold this module's content.** This is
the numbering drift the reconciliation map (F-001) exists to track. Don't let
the matching directory name (`m2`) fool you into assuming a matching spine
module.

On-disk contents of `assignments/m2/` (all present, all left exactly as-is —
not touched by this pass):

- `README.md` — legacy module README, titled "Module 2: User Input and
  Advanced Calculations."
- `M2T1_InteractiveMarketplace.md`
- `M2T2_RestaurantCalculator.md`
- `M2LAB1_CrateManufacturing.md`
- `M2HW1_MultiProgramChallenge.md`

**What this content actually is:** `cin`/`cout`, input validation basics,
`iomanip` formatting, arithmetic/percentage calculations, multi-step business
logic — i.e., spine **M3 (Program Basics)** content (I/O, arithmetic; see
spine ~line 161–176 and CCL crosswalk row "Input/output operations |
M3 (core)"). Per the module-identity map
(`_tracking/numbering-reconciliation-map.md`, moduleIdentities), both
`assignments/m1/*` and `assignments/m2/*` are recorded as spine-M3's
Program-Basics content, pending the F-001 port + rename — **owned by
`modules/m3/`, not this module.**

**Nothing from `assignments/m2/` is slotted into `modules/m2/`.** Spine M2
("How to Solve Problems") has no legacy on-disk predecessor at all — per the
module-identity map it is marked **NEW** in full: Hello World tour, error
taxonomy, flowcharts/pseudocode/user stories, `thinkcpp` + Communication
decks (see asset table above). This ledger entry exists so a future reader
who sees "`assignments/m2/`" and "`modules/m2/`" side by side does not assume
they are the same module under old/new numbering.

---

## Numbering flags (pending reconciliation — not resolved here)

1. **THE BIG ONE.** `assignments/m1/*` + `assignments/m2/*` legacy content
   maps to spine **M3**, while spine **M1** and **M2** are net-new modules
   with no legacy directory at all. This module (`modules/m2/`) is
   unaffected in terms of *content* — nothing to port in. But the *directory
   name collision* (`assignments/m2/` vs. `modules/m2/`) is exactly the kind
   of drift a future contributor could misread as "the same module, just
   moved." This is flagged here per the skeleton plan's non-clobber policy,
   so the ledger is discoverable from either side.
2. **Open question ownership.** The actual port-and-renumber of
   `assignments/m1/*` and `assignments/m2/*` into `modules/m3/` is
   `modules/m3/_assets.md`'s open question to carry (per
   `_tracking/numbering-reconciliation-map.md` and
   `_tracking/skeleton-plan.md` §5.1), **not this module's.** That includes
   deciding whether all ten legacy deliverables survive as M3 artifacts, or
   some get trimmed or reassigned. Recorded here only as a cross-reference so
   a reader of `modules/m2/` isn't left wondering where the "obvious"
   `assignments/m2/` content went.
3. **Ratify-the-namespace open question** (`_tracking/skeleton-plan.md` §5.2)
   is a spine-owner ruling, not something this module resolves: whether the
   two-tree model (`modules/` canonical + `assignments/` frozen) is the final
   call, or `assignments/` gets renamed into spine order first.
