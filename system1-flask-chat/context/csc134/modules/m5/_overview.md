# M5 — Loops

**Phase:** D · **Weeks:** ~Weeks 7–8 *(the End Boss — Week 8 is the designated
light buffer; Loops is the natural place to absorb it)*

**Big idea:** Iteration — repetition as a decomposition tool.

> Verbatim from the spine (`_storming/CSC-134-course-spine.md`, "## M5 — Loops"):
> `while`, `do-while`, `for`; input validation (the `cin` fail-state,
> bulletproofing); nested loops; the professional menu pattern. Verification
> gets real: **trace tables and predict-then-run.** The turtle bridge is the
> visual *Learn* anchor (a body that repeats + a count) before the numeric
> versions.

---

## LPAA beat map

| Beat | One-liner (from spine) |
|---|---|
| **Learn** | *Chapter 5 / Module 04* reading; the turtle square as the iteration anchor (a body that repeats + a count) before the numeric loop forms. |
| **Practice** | Exit ticket — predict loop output; spot the off-by-one. |
| **Apply** | Instructor-led — type in the **Level Up Stats** `for` loop, get the table aligned; *then the Make gradient opens:* "here's 80% of the menu system — finish the validation loop." |
| **Assess** | Loop fundamentals (`while` / `for` / array-search) + Project 2, the menu-driven game (tiered C/B/A). |

Full acceptance-criteria skeleton for the Assess beat lives in
`_assess-spec.STUB.md` (this file only carries the one-liner). MLOs live in
`_mlos.md`. Asset provenance and the legacy-content ledger live in
`_assets.md`.

---

## Make-gradient position

**M5 sits at the top of the M5–M7 band: finish-the-80%.** This is the seam
module — the Apply beat is *split* in two parts per the spine:

1. **Type-in first** (the M2–M4 shape, carried over one more module): the
   **Level Up Stats** `for` loop, typed in full, table aligned and running
   clean.
2. **Then the gradient opens for the rest of the module:** the menu system
   arrives ~80% built (the `_contracts/m5_menu.cpp` shape); the student
   finishes the validation loop.

Do not drift this position when the Apply tutorial is authored: M5 is not a
type-in-100% module like M3/M4, and it is not a spec-only module like M8. The
80%-scaffold shape is specific to *the menu/validation half* of the module,
not the Level Up Stats warm-up.

---

## User story (fill-in — deep-build authors this against the actual M4 exit state)

> As a student finishing M4 (Decisions), I want ________________, so that
> ________________.

*(Seed thought, not the authored answer: M4 leaves a student able to write a
program that makes one decision and stops — the Dungeon Gatekeeper checks a
character once, then the program ends. M5 changes that: the program keeps
running until the *player* decides to stop. And "ask again if that input was
garbage" turns from a lucky accident into a taught pattern.)*

---

## Canonical home

**This file, and the rest of `modules/m5/`, is the canonical spine-truth home
for M5.** `assignments/` is legacy source — frozen, not a scaffold target. See
`_assets.md` for exactly which legacy files hold M5's pre-existing content and
what porting them into this tree will require. Nothing under `assignments/`
was moved, renamed, or edited to produce this scaffold.

---

## Contracts touched

None edited. This is a structure-only skeleton pass — no Learn/Practice/Apply/
Assess content authored, no edits to `_contracts/`, `_storming/`, `_tracking/`,
or `assignments/`. `_contracts/m5_menu.cpp` is read-referenced but not
modified. It's M5's canonical Apply/Assess anchor — the M4 gatekeeper wrapped
in a validated menu loop.
