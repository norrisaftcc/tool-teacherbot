# M8 — Capstone Miniproject

**Phase:** F · **Weeks:** ~Weeks 14–16

**Big idea:** The whole arc, run once, end to end, by you. The final exam is
the spine *performed*.

> Verbatim from the spine (`_storming/CSC-134-course-spine.md`, "## M8 —
> Capstone Miniproject"): a three-part structure — **problem formulation**
> (front-loaded and graded heavily: problem statement, user stories, spec,
> flowchart — a design document due before any code) → **implementation**
> (AI assistance permitted per the course's ladder; the student owns the
> problem definition and the verification; built in stages, each of which
> compiles and runs as a standalone program) → **presentation** (demo working
> software; explain what it does, what decisions were made, and show it meets
> the spec). The RPG/dungeon theme that ran all term pays off here, and the
> project builds on the structs and classes from M7.

---

## LPAA beat map

| Beat | One-liner (from spine) |
|---|---|
| **Learn** | No new reading content named by the spine for M8 itself — M8 draws on every prior Learn beat (M0–M7) as its input. The "reading" at this stage is the student's own design document once drafted. |
| **Practice** | Not a traditional module exit ticket — the spine frames the design document itself as the front-loaded, heavily-graded checkpoint that gates entry into implementation (see MLO 8.1). |
| **Apply** | **Spec-only** (the Make-gradient's endpoint). No instructor-led type-in and no 80%-built starting program — the student is handed a spec for what the design document and staged build must contain, not a codebase to extend. |
| **Assess** | The capstone itself: design doc (graded heavily) + staged implementation + presentation/defense, including any AI assistance documented. Full acceptance-criteria skeleton lives in `_assess-spec.STUB.md`. |

MLOs live in `_mlos.md`. Asset provenance and the legacy-content ledger live
in `_assets.md`.

---

## Make-gradient position

**M8 sits alone at the end of the Make gradient: spec-only.** M2–M4 handed
students 100% to type in; M5–M7 handed them ~80% to finish. M8 hands them
**a spec** — a problem-formulation requirement and a staged-build
requirement — and nothing pre-built to extend. This is the intended and
final position on the gradient, not a gap to fill with more scaffolding.
Do not backfill M8 with a starter codebase or a type-in tutorial; the
absence of one *is* the pedagogy ("assessment logic: we grade the two things
AI cannot do for you — knowing what to build, and standing behind what you
built").

---

## User story (fill-in — deep-build authors this against the actual M7 exit state)

> As a student finishing M7 (Structured Data & Objects), I want
> ________________, so that ________________.

*(Seed thought, not the authored answer: M7 leaves a student able to model
data with structs, pass it by reference, and grow a struct into a class with
encapsulated behavior — but every prior module handed that student either a
full program to type in or a mostly-built program to finish. M8 is the first
time the student must decide *what to build at all*: write their own problem
statement and user stories, design their own struct/class shapes, and defend
the result. The gap M8 closes is not a C++ syntax gap — it's the "own the
problem, not just the code" gap the spine names directly.)*

---

## Canonical home

**This file, and the rest of `modules/m8/`, is the canonical spine-truth
home for M8.** `assignments/` is legacy source — frozen, not a scaffold
target (see `_assets.md` in this folder for exactly which legacy/ported
assets hold M8's pre-existing content and what porting them into this tree
will require). Nothing under `assignments/` was moved, renamed, or edited to
produce this scaffold. Note: as of this pass, `assignments/m8/` does not
exist on disk — only `assignments/m0/`, `m1/`, and `m2/` are populated — so
M8 has no legacy folder of its own to record content already sitting under
its own number; the stale course-manifest's `M08` entry names two
project-shaped deliverables that plausibly belong here, tracked in
`_assets.md` per F-001's not-yet-imported status.

---

## Contracts touched

None. This is a structure-only skeleton pass — no Learn/Practice/Apply/Assess
content authored, no edits to `_contracts/`, `_storming/`, `_tracking/`, or
`assignments/`.
