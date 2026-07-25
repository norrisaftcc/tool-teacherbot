# M4 — Decisions

**Phase:** D · **Weeks:** ~Weeks 5–6

**Big idea:** Selection — the diamonds from M2's flowcharts, made executable.

> Verbatim from the spine (`_storming/CSC-134-course-spine.md`, "## M4 —
> Decisions"):
> `if` / `else if` / `else`; `switch`; comparison and logical operators;
> nested conditions. This is where **"filters" (CCL)** begins — conditionally
> processing input. Assignments start from a flowchart and end in code; at
> least once, the reverse (read code, recover the flowchart).

---

## LPAA beat map

| Beat | One-liner (from spine) |
|---|---|
| **Learn** | *Chapter 4 / Module 03* reading. |
| **Practice** | Exit ticket — trace which branch runs for given inputs. |
| **Apply** | Instructor-led — type in a build-your-own-adventure decision program. |
| **Assess** | A decision lab from spec (the CYOA theme carries the branching lesson twice — in the content *and* in the structure). |

Full acceptance-criteria skeleton for the Assess beat lives in
`_assess-spec.STUB.md` (this file only carries the one-liner). MLOs live in
`_mlos.md`. Asset provenance and the legacy-content ledger live in
`_assets.md`.

---

## Make-gradient position

**M4 sits at the top edge of the M2–M4 band: type-in 100%.** The Apply beat
hands students the full build-your-own-adventure decision program. They type
it in character by character and get it compiling and running clean — no
scaffolding gaps to fill. M4 is the *last* module at this position. The
gradient shifts to "here's 80%, finish it" starting at M5. Do not drift this
position when the Apply tutorial is authored. Do not borrow M5's
finish-the-80% shape early.

---

## User story (fill-in — deep-build authors this against the actual M3 exit state)

> As a student finishing M3 (Program Basics), I want ________________, so
> that ________________.

*(Seed thought, not the authored answer: M3 leaves a student able to write a
program that reads input, does arithmetic, and prints formatted output. That's
one straight-line path through `main` — no branching, no "different input,
different behavior." Every M3 program runs the same way no matter what the
user types. M4 is where the program starts *choosing*. The flowchart diamonds
a student has been drawing since M2 finally become code that actually
forks.)*

---

## Canonical home

**This file, and the rest of `modules/m4/`, is the canonical spine-truth home
for M4.** `assignments/` is legacy source — frozen, not a scaffold target.
Unlike M3, there is **no legacy `assignments/m4/` directory at all** — the
legacy tree only holds `m0`, `m1`, `m2`. M4's pre-existing content instead
lives under `_past_work/_claudes_input/03-decisions-week5-6/` and
`_storming/`. See `_assets.md` for exactly which files those are and what
porting them into this tree will require. Nothing under `assignments/`,
`_past_work/`, or `_storming/` was moved, renamed, or edited to produce this
scaffold.

---

## Contracts touched

None edited. This is a structure-only skeleton pass — no Learn/Practice/
Apply/Assess content authored, no edits to `_contracts/`, `_storming/`,
`_tracking/`, or `assignments/`. Note for deep-build: M4's Assess artifact
will build **against** the frozen `_contracts/m4_gatekeeper.cpp` (the
canonical Dungeon Gatekeeper decision program — read, not modified, during
this pass). See `_assets.md` for its `CONTRACT` tag and the seam it sets up
for M5's `_contracts/m5_menu.cpp`.
