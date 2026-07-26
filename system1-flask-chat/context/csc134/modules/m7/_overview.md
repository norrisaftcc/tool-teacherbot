# M7 — Structured Data & Objects

**Phase:** E · **Weeks:** ~Weeks 11–13

**Big idea:** Aggregate data — and the struct→class arc. *A class is a struct
that also has behavior.* OOP lands here, time-aligned with CTI's complex-data
module.

> Verbatim from the spine (`_storming/CSC-134-course-spine.md`, "## M7 —
> Structured Data & Objects"): a deliberate five-step progression — **raw
> arrays** (declare/initialize/traverse; array/index vs. value) →
> **parallel arrays** (used intentionally as a stepping stone, with in-code
> comments flagging the future refactor) → **structs** (bundle related data;
> the parallel arrays collapse into one clean array of structs) →
> **pointers** (introduced in context — passing structs by reference, the
> array/pointer relationship — not a standalone unit) → **classes/OOP**
> (encapsulation and methods; the struct grows behavior and becomes a class).

---

## LPAA beat map

| Beat | One-liner (from spine) |
|---|---|
| **Learn** | Readings on arrays, structs, classes. |
| **Practice** | Exit tickets — array indexing (`i` vs `i+1`); struct member access; when a reference is needed. |
| **Apply** | Instructor-led — build a `Room` struct array; "here's 80% of the `Hero` class — finish the methods." |
| **Assess** | The tiered `M7LAB1` — C: refactor parallel arrays into a `Room` struct array; B: add a `Hero` struct to teach pass-by-value vs. pass-by-reference; A: add a `Monster` struct with auto-resolve combat; then a class refactor. |

Full acceptance-criteria skeleton for the Assess beat lives in
`_assess-spec.STUB.md` (this file only carries the one-liner). MLOs live in
`_mlos.md`. Asset provenance and the legacy-content ledger live in
`_assets.md`.

---

## Make-gradient position

**M7 sits in the M5–M7 band: finish-the-80%.** The Apply beat hands students
a mostly-working program — the `Room` struct array built together, then
"here's 80% of the `Hero` class" — and the missing piece is what they
complete. This is not a full type-in (that band closed at M4), and it is not
a spec-only build (that starts at M8). Do not drift this position when the
Apply tutorial is authored: a full type-in-100% shape belongs to M2–M4, and a
spec-only handoff belongs to M8, not M7.

---

## User story (fill-in — deep-build authors this against the actual M6 exit state)

> As a student finishing M6 (Functions), I want ________________, so that
> ________________.

*(Seed thought, not the authored answer: M6 leaves a student able to
decompose a working program into functions with prototypes, parameters, and
return values — but every function that operates on "a monster's name AND
its hp AND its attack" still juggles those as separate, same-indexed
variables or parallel arrays, with no language feature binding them
together. M7 is where the data itself gets a shape: a struct that carries
its own fields, then a class that carries its own behavior too.)*

---

## Canonical home

**This file, and the rest of `modules/m7/`, is the canonical spine-truth home
for M7.** `assignments/` is legacy source — frozen, not a scaffold target
(see `_assets.md` in this folder for exactly which legacy/ported assets hold
M7's pre-existing content and what porting them into this tree will require).
Nothing under `assignments/` was moved, renamed, or edited to produce this
scaffold. Note: as of this pass, `assignments/m7/` does not exist on disk — only
`assignments/m0/`, `m1/`, and `m2/` are populated. So M7 has no legacy folder
holding content already filed under its own number. Its named source assets
(`M6LAB2`, `M7LAB1`, *Terminal Graphics*, *Turtle→Spaghetti*) are tracked
instead in `_assets.md`, per F-001's not-yet-imported status for all four.

---

## Contracts touched

None. This is a structure-only skeleton pass — no Learn/Practice/Apply/Assess
content authored, no edits to `_contracts/`, `_storming/`, `_tracking/`, or
`assignments/`.
