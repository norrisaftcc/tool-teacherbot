# M3 — Module Learning Objectives (skeleton)

**Status:** skeleton slots only — not authored objectives. Derived from
`_storming/CSC-134-course-spine.md` ("## M3 — Program Basics") and
`_storming/CSC-134-learning-objectives.md` ("### M3 — Program Basics").
Deep-build fills in beat-level detail. This file records the MLO shape and its
CLO/CCL wiring, so downstream beats (Learn/Practice/Apply/Assess) build against
the same targets.

---

## MLO slots (feeding the CLOs)

| MLO | Statement (from the learning-objectives doc) | Feeds |
|---|---|---|
| **MLO 3.1** | Declare and use variables of appropriate data types. | → CLO2 (I/O & arithmetic) |
| **MLO 3.2** | Write programs that perform input, processing, and output using arithmetic expressions. | → CLO2 (I/O & arithmetic) |
| **MLO 3.3** | Locate and correct errors by reading compiler and runtime messages. | → CLO7 (Test & debug) |

*Measured by (per the objectives doc):* the I/O + arithmetic lab (e.g., Pizza
Calculator). The Assess-beat spec stub (`_assess-spec.STUB.md`) is where this
gets turned into testable acceptance criteria.

---

## CCL crosswalk touch (this module)

Per the spine's M3 section: **input/output operations; arithmetic operations.**

CLO coverage-matrix row for M3 (from the learning-objectives doc's coverage
matrix, I=Introduced / D=Developed / M=Mastered):

| CLO | M3 |
|---|:--:|
| CLO1 — Design & represent | — |
| CLO2 — I/O & arithmetic | **D** |
| CLO3 — Selection & iteration | — |
| CLO4 — Functions | — |
| CLO5 — Arrays/structs/pointers | — |
| CLO6 — Objects / classes | — |
| CLO7 — Test & debug | **D** |
| CLO8 — Communicate & AI use | **D** |

M3 develops CLO2, CLO7, and CLO8. It does not introduce or master any CLO on
its own — CLO2 and CLO8 were introduced in M0/M1, and CLO7 was introduced in
M2. All CLOs master at M8's capstone.

---

## Slots pending deep-build authoring

- [ ] Per-MLO "what a student can do" behavioral statement (beyond the spine's
      one-line summary above).
- [ ] Mapping each MLO to the specific Learn/Practice/Apply/Assess artifact
      that measures it (Assess is stubbed in `_assess-spec.STUB.md`; Learn/
      Practice/Apply are not yet built).
- [ ] Confirming MLO 3.3's error-taxonomy scope for M3 specifically. All four
      words are in play course-wide by M2, per the spine's error taxonomy
      table. M3's "Debugging as curriculum" framing is where students first
      *practice* reading real compiler/runtime messages against a program they
      wrote themselves — not just classify an error someone else hands them.
