# M1 — Asset-slotting notes

Tags: **PORT** (adapt an existing asset), **NEW** (author fresh), **CONTRACT**
(build against a frozen `_contracts/` file). Per the spine's asset table
(`_storming/CSC-134-course-spine.md` line ~132, ~372) and the skeleton-layout
plan's module-identity table (`_tracking/skeleton-plan.md`).

## Assets slotting into this module

| Asset | Tag | Source | Notes |
|---|---|---|---|
| Robot Sandwich assignment | **PORT** | CTI (shared course) | "Adopted essentially unchanged — it contains no code" per spine. This is M1's Assess-beat artifact (see `_assess-spec.STUB.md`). Ownership question (who maintains the shared copy, in which repo) is spine open item #6 (`_storming/CSC-134-course-spine.md` line ~379) — not resolved here. |
| Robot-Sandwich explainer decks (linear + choose-your-own) | **PORT** | CTI (shared course) | The Communication-thread hook; feeds the Learn/Practice beats. Two variants noted in spine — deep-build decides which (or both) to use. |
| Markdown reading content (why Markdown, why LLMs made it ubiquitous) | **NEW** | — | No existing asset identified in the spine's asset table for this specific angle; author fresh in deep-build. |
| Repo/README/commit/push Apply-beat walkthrough | **NEW** | — | Instructor-led workflow demo; no ported asset named in the spine — author fresh, keyed to Codespaces-as-equalizer requirement. |
| Rubric shape (Correctness/Completeness/Format/Submission) | **CONTRACT** | `_contracts/rubric-template.md` | M1's Robot Sandwich is the spine's stated *origin point* for this template (line ~296: "descended from the Robot Sandwich's four columns") — M1 both consumes and historically anchors this contract. Column one is Correctness per ADR-002. |

No `_contracts/*.cpp` code contract applies to M1 — it is the only module
besides M0 with no C++ artifact at all.

---

## Legacy-content ledger (drifted on-disk content — recorded, not moved)

**`assignments/m1/` exists on disk today and is NOT this module's content.**
Per `_tracking/numbering-reconciliation-map.md` (F-001, rename-map row 7 /
open question 7) and the skeleton-layout plan, `assignments/m1/` physically
holds **spine-M3 (Program Basics)** material — variables, `cin`/`cout`,
arithmetic — carried under an old textbook-order numbering scheme that
predates the current spine's M1/M2/M3 split.

| File on disk (`assignments/m1/`) | Actual spine home | Status |
|---|---|---|
| `README.md` | M3 (Program Basics) | Legacy, frozen — left exactly as-is. |
| `M1T1_HelloWorld.md` | M3 | Legacy, frozen. |
| `M1T2_DigitalBusinessCard.md` | M3 | Legacy, frozen. |
| `M1LAB_CoffeeShopPOS.md` | M3 | Legacy, frozen. |
| `M1HW1_StudentBudgetAnalyzer.md` | M3 | Legacy, frozen. |

**Nothing above is ported into `modules/m1/`.** These five files are recorded
here only so a future reader of `modules/m1/` isn't misled by the matching
"M1" number on disk. The true spine-M1 content (Robot Sandwich, Markdown,
repo workflow) has no legacy on-disk predecessor — it is genuinely **NEW**
material. The actual port target for these five files is **`modules/m3/`**,
whose own `_assets.md` should carry the mirror image of this entry
(`assignments/m1/*` + `assignments/m2/*` → M3, per F-001). This module does
not act on that port — only records the cross-reference.

---

## Numbering flags

1. **Directory-name collision, not content collision.** `assignments/m1/`
   and `modules/m1/` share a number but hold entirely different modules'
   content (legacy-M3 vs. spine-true-M1). This is the core F-001 finding.
   Flagging it here again, at the point of construction, so it's visible
   from inside the canonical M1 tree itself — not only in the
   reconciliation map.
2. **F-001 rename not actioned.** Per the non-clobber policy, this pass does
   not move, rename, or edit `assignments/m1/*`. The rename (into
   `modules/m3/`, likely with new `M3*`-style filenames) lands later, owned
   by whoever builds M3.
3. **Open question inherited, not resolved:** do all five legacy
   `assignments/m1/*` files, plus the parallel `assignments/m2/*` files,
   survive intact as M3 artifacts — or are some trimmed or reassigned?
   That's reconciliation-map open question 7, a content-scope call for the
   M3 builder/spine-owner. It's out of scope for this M1 skeleton.

---

## Cross-references

- `_tracking/numbering-reconciliation-map.md` — full F-001 findings.
- `_tracking/skeleton-plan.md` — module-identity table, non-clobber policy.
- `_storming/CSC-134-course-spine.md` — asset table (line ~372), M1 section
  (line ~118).
- `modules/m1/_overview.md`, `modules/m1/_mlos.md`,
  `modules/m1/_assess-spec.STUB.md` — sibling skeleton files.
