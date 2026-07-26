# M1 — Talk to Computers (and Your Team)

> **Canonical home.** This `modules/m1/` tree is the spine-true scaffold for M1.
> `assignments/m1/` is **legacy** and holds drifted content that actually belongs
> to spine **M3** (Program Basics) — see this module's `_assets.md` and
> `_tracking/numbering-reconciliation-map.md` (F-001) for the full reconciliation.
> Do not treat `assignments/m1/` as this module's home; it is a different module's
> content sitting under an old number.

**Spine header**

| Field | Value |
|---|---|
| Module | M1 |
| Title | Talk to Computers (and Your Team) |
| Phase | B |
| Weeks | ~Weeks 1–2 |
| Sequence position | 2nd module (after M0, before M2) |

**Big idea** (verbatim from `_storming/CSC-134-course-spine.md`):
> Plain text is the native language of both programming and professional
> collaboration. Precise instructions come *before* code.

**Content anchor:** VSCode as a programmer's editor (vs. Word); the markup
ladder `.txt → .md → .html`; GitHub's own Markdown docs as the authoritative
reference; the pull → commit → push submission workflow; Codespaces as the
equalizer (the only way to work for a student on a Chromebook — access is a
design requirement, not a convenience).

**Spine connection:** Decomposition and precise communication, before any code
exists to hide behind.

---

## LPAA beat map (skeleton — not yet authored)

| Beat | One-liner from spine |
|---|---|
| **Learn** | Markdown reading; why it exists; why LLMs made it ubiquitous. |
| **Practice** | Exit ticket on Markdown syntax + the commit/push cycle. |
| **Apply** | Instructor-led — make a repo, write a real `README.md`, commit, push, preview it on GitHub. |
| **Assess** | The Robot Sandwich (shared with CTI, adopted essentially unchanged — it contains no code). |

---

## Make-gradient position

**M1 sits before the Make-gradient's code-scaffold ladder starts.** The
gradient (M2–M4 type-in-100% / M5–M7 finish-the-80% / M8 spec-only) governs
how much *C++ code* the Apply beat pre-builds for the student. M1 has no C++
yet — its Apply beat is instructor-led repo/README/commit/push, prose and
Markdown, not code. Record this explicitly so no downstream builder mistakes
M1 for a type-in-100% C++ module: **M1's Apply beat is instructor-led
workflow, pre-gradient.** The gradient's first module is M2.

**Note (ADR-004 consistency):** M1's Apply beat is repo → README → commit →
push, **no branch**. This matches the student-flow git convention
(commit + push only, no PRs before capstone) — do not introduce branching
here.

---

## User-story fill-in

> As a student finishing **M0 (Welcome to Programming)**, I want
> ____________________, so that ____________________.

*(Skeleton only — the deep-build pass fills this in from the M0→M1 seam:
the student has a working toolchain and a "hello world" that compiles: what
do they now need in order to communicate precisely, before writing more
code?)*

---

## Cross-references

- Spine section: `_storming/CSC-134-course-spine.md` — grep `## M1 —`
  (line ~118).
- Rubric contract: `_contracts/rubric-template.md` (four columns, four tiers;
  M1's Robot Sandwich is the template's origin point per the spine).
- Asset ledger: `modules/m1/_assets.md` (this module).
- Legacy/numbering: `_tracking/numbering-reconciliation-map.md` (F-001).
