# M6 — Functions

**Phase:** D · **Weeks:** ~Weeks 9–10

**Big idea:** Decomposition made literal — the Robot Sandwich steps become
named, reusable, testable units. Code is *revised*, not just written.

> Verbatim from the spine (`_storming/CSC-134-course-spine.md`, "## M6 —
> Functions"): defining and calling functions; the **single-file convention
> completed** (prototypes at top, `main` in the middle, definitions at the
> bottom); parameters, return values; **pass-by-value vs. pass-by-reference**;
> scope basics. Signature move: **refactor a prior M4 or M5 program into
> functions** — same behavior, better structure.

---

## LPAA beat map

| Beat | One-liner (from spine) |
|---|---|
| **Learn** | *Chapter 3 / Module 02* reading. *(Authored as "Chapter 3," delivered here, after loops — see sequencing note below.)* |
| **Practice** | Exit ticket — predict what a function returns; identify scope. |
| **Apply** | Instructor-led — extract functions from a monolithic program; "here's 80% — write the missing functions to match these prototypes." |
| **Assess** | The refactor lab — take your M5 program and decompose it into functions. |

Full acceptance-criteria skeleton for the Assess beat lives in
`_assess-spec.STUB.md` (this file only carries the one-liner). MLOs live in
`_mlos.md`. Asset provenance and the legacy-content ledger live in
`_assets.md`.

---

## Make-gradient position

**M6 sits in the M5–M7 band: here's-80%-finish-it.** The Apply beat hands
students a mostly-working program with the function *prototypes* given and one
or more function *bodies* missing — the student writes the missing
definitions to match the stated signatures. This is not M2–M4's type-in-100%
(there is no full-program-from-scratch typing exercise here) and it is not
M8's spec-only (the shape of the solution — the prototypes — is given, not
invented). Do not drift this position when the Apply tutorial is authored.

---

## User story (fill-in — deep-build authors this against the actual M5 exit state)

> As a student finishing M5 (Loops), I want ________________, so that
> ________________.

*(Seed thought, not the authored answer: M5 leaves a student able to write a
menu-driven program with a validated input loop — but that program is one long
`main`, and the student has felt the pain of scrolling through 80+ lines to
find the one block they need to fix. M6 is where the program's mass gets
sorted into named, callable pieces — the same behavior, but findable and
revisable. The frozen `_contracts/m5_menu.cpp` is the exact "M5-shaped
program" this module's signature refactor move starts from.)*

---

## Canonical home

**This file, and the rest of `modules/m6/`, is the canonical spine-truth home
for M6.** `assignments/` is legacy source — frozen, not a scaffold target (see
`_assets.md` for exactly which legacy/`_past_work/` files hold M6's
pre-existing content and what porting them into this tree will require).
Nothing under `assignments/` or `_past_work/` was moved, renamed, or edited to
produce this scaffold. Note: `assignments/m6/` does not currently exist on
disk — there is no legacy directory of that name to reconcile against, unlike
M3's `assignments/m1`/`m2` situation.

---

## Contracts touched

None edited. This is a structure-only skeleton pass — no Learn/Practice/
Apply/Assess content authored, no edits to `_contracts/`, `_storming/`,
`_tracking/`, or `assignments/`. **Read-only reference note:** `_contracts/
m5_menu.cpp`'s own header comment states "M6 refactors it into functions" —
this frozen file is the strong candidate canonical input for M6's Assess-beat
refactor lab (see `_assess-spec.STUB.md`) and `_contracts/rubric-template.md`
is the frozen rubric shape every M6 lab tier ladder inherits. Neither file was
modified by this pass.
