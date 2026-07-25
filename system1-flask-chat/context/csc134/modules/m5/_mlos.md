# M5 — Module Learning Objectives (skeleton)

**Status:** skeleton slots only — not authored objectives. Derived from
`_storming/CSC-134-course-spine.md` ("## M5 — Loops") and
`_storming/CSC-134-learning-objectives.md` ("### M5 — Loops"). Deep-build
fills in beat-level detail; this file records the MLO shape and its CLO/CCL
wiring so downstream beats (Learn/Practice/Apply/Assess) build against the
same targets.

---

## MLO slots (feeding the CLOs)

| MLO | Statement (from the learning-objectives doc) | Feeds |
|---|---|---|
| **MLO 5.1** | Implement iteration using `while`, `do-while`, and `for` loops. | → CLO3 (Selection & iteration) |
| **MLO 5.2** | Validate user input and prevent common loop failures (infinite loops, `cin` fail state). | → CLO3, CLO7 (Test & debug) |
| **MLO 5.3** | Predict loop output using a trace table before running the program. | → CLO7 (Test & debug) |
| **MLO 5.4** | Combine loops and selection to filter and process a sequence of data. | → CLO3 |

*Measured by (per the objectives doc):* loop fundamentals (`while`/`for`/
array-search) + Project 2, the menu-driven game. The Assess-beat spec stub
(`_assess-spec.STUB.md`) is where this gets turned into testable acceptance
criteria.

---

## CCL crosswalk touch (this module)

Per the spine's M5 section: **iteration; filters (loop-and-select over
streams).**

CLO coverage-matrix row for M5 (from the learning-objectives doc's coverage
matrix, I=Introduced / D=Developed / M=Mastered):

| CLO | M5 |
|---|:--:|
| CLO1 — Design & represent | — |
| CLO2 — I/O & arithmetic | — |
| CLO3 — Selection & iteration | **I** *(loops introduced here; selection itself was introduced M4)* |
| CLO4 — Functions | — |
| CLO5 — Arrays/structs/pointers | — |
| CLO6 — Objects / classes | — |
| CLO7 — Test & debug | **D** |
| CLO8 — Communicate & AI use | **D** |

*(Confirm the exact letters against the learning-objectives doc's own
coverage-matrix row for M5 at deep-build time. This file transcribes the
per-module MLO list, which is the primary source. The matrix table itself
lives further down that same document; this skeleton pass did not recopy it
cell-by-cell.)*

M5 introduces the iteration half of CLO3 (selection was introduced in M4) and
develops CLO7 and CLO8. No CLO masters at M5 — all CLOs master at M8's
capstone.

---

## Slots pending deep-build authoring

- [ ] Per-MLO "what a student can do" behavioral statement (beyond the
      spine's one-line summary above).
- [ ] Mapping each MLO to the specific Learn/Practice/Apply/Assess artifact
      that measures it (Assess is stubbed in `_assess-spec.STUB.md`; Learn/
      Practice/Apply are not yet built).
- [ ] Confirming MLO 5.3's "trace table" artifact shape — spine calls out
      "trace tables and predict-then-run" as verification getting real at M5;
      deep-build decides whether the trace table is a Practice-beat
      (exit-ticket) artifact, an Apply-beat scaffold element, or both.
- [ ] Confirming MLO 5.4's exact Assess-beat home. "Combine loops and
      selection to filter a sequence" is the array-search half of the Assess
      line. Deep-build should verify this doesn't silently drift into M7
      (Structured Data & Objects) territory, which owns arrays proper.
