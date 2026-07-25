# M7 — Module Learning Objectives (skeleton)

**Status:** skeleton slots only — not authored objectives. Derived from
`_storming/CSC-134-course-spine.md` ("## M7 — Structured Data & Objects") and
`_storming/CSC-134-learning-objectives.md` ("### M7 — Structured Data &
Objects"). Deep-build fills in beat-level detail; this file records the MLO
shape and its CLO/CCL wiring so downstream beats (Learn/Practice/Apply/
Assess) build against the same targets.

---

## MLO slots (feeding the CLOs)

| MLO | Statement (from the learning-objectives doc) | Feeds |
|---|---|---|
| **MLO 7.1** | Declare, initialize, and traverse arrays. | → CLO5 (Arrays/structs/pointers) |
| **MLO 7.2** | Model related data using structs and access their members. | → CLO5 (Arrays/structs/pointers) |
| **MLO 7.3** | Use pointers to pass and modify structured data by reference. | → CLO5 (Arrays/structs/pointers) |
| **MLO 7.4** | Design and use a class that encapsulates data and behavior. | → CLO6 (Objects / classes) |

*Measured by (per the objectives doc):* the tiered `M7LAB1` (Room struct →
Hero → Monster → class refactor). The Assess-beat spec stub
(`_assess-spec.STUB.md`) is where this gets turned into testable acceptance
criteria.

---

## CCL crosswalk touch (this module)

Per the spine's M7 section: **arrays; pointers; object-oriented
programming.**

CLO coverage-matrix row for M7 (from the learning-objectives doc's coverage
matrix, I=Introduced / D=Developed / M=Mastered):

| CLO | M7 |
|---|:--:|
| CLO1 — Design & represent | — |
| CLO2 — I/O & arithmetic | **D** |
| CLO3 — Selection & iteration | **D** |
| CLO4 — Functions | **D** |
| CLO5 — Arrays/structs/pointers | **I · D** |
| CLO6 — Objects / classes | **I** |
| CLO7 — Test & debug | **D** |
| CLO8 — Communicate & AI use | **D** |

M7 is the **first** module to touch CLO5 and CLO6 at all — both show blank in
every earlier column. It introduces *and* develops CLO5 in the same module
(arrays → structs → pointers is a full arc within M7 itself), and it
introduces CLO6 (objects/classes), which then only develops further at the M8
capstone. This makes M7 the heaviest single-module CLO onboarding in the
spine outside M8 itself — a note for deep-build pacing, not a change to the
matrix.

---

## Slots pending deep-build authoring

- [ ] Per-MLO "what a student can do" behavioral statement (beyond the
      spine's one-line summary above).
- [ ] Mapping each MLO to the specific Learn/Practice/Apply/Assess artifact
      that measures it (Assess is stubbed in `_assess-spec.STUB.md`; Learn/
      Practice/Apply are not yet built).
- [ ] Confirming how MLO 7.3 (pointers) is scoped for exit-ticket
      Practice-beat items — the spine is explicit that pointers are "not a
      standalone unit," so Practice items must test the in-context use
      (pass-a-struct-by-reference), not free-standing pointer arithmetic.
- [ ] Resolving F-001's open question on the STL/`std::string` and File I/O
      legacy manifest content (see `_assets.md`) before deep-build decides
      whether either has any place inside M7's scope, given the spine names
      neither.
