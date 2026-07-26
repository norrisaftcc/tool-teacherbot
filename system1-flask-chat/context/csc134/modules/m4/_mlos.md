# M4 — Module Learning Objectives (skeleton)

**Status:** skeleton slots only — not authored objectives. Derived from
`_storming/CSC-134-course-spine.md` ("## M4 — Decisions") and
`_storming/CSC-134-learning-objectives.md` ("### M4 — Decisions"). Deep-build
fills in beat-level detail; this file records the MLO shape and its CLO/CCL
wiring so downstream beats (Learn/Practice/Apply/Assess) build against the
same targets.

---

## MLO slots (feeding the CLOs)

| MLO | Statement (from the learning-objectives doc) | Feeds |
|---|---|---|
| **MLO 4.1** | Implement selection using `if` / `else if` / `else` and `switch`. | → CLO3 (Selection & iteration) |
| **MLO 4.2** | Construct boolean expressions using comparison and logical operators. | → CLO3 (Selection & iteration) |
| **MLO 4.3** | Translate a flowchart's decision points into working code, and recover a flowchart from existing code. | → CLO1 (Design & represent), CLO3 (Selection & iteration) |

*Measured by (per the objectives doc):* the decision-structures (CYOA) lab.
The Assess-beat spec stub (`_assess-spec.STUB.md`) is where this gets turned
into testable acceptance criteria.

---

## CCL crosswalk touch (this module)

Per the spine's M4 section: **filters (selection over data)** — this is the
module where "filters" (conditionally processing input) begins as a named
CCL concept.

CLO coverage-matrix row for M4 (from the learning-objectives doc's coverage
matrix, I=Introduced / D=Developed / M=Mastered):

| CLO | M4 |
|---|:--:|
| CLO1 — Design & represent | **D** |
| CLO2 — I/O & arithmetic | **D** |
| CLO3 — Selection & iteration | **I** |
| CLO4 — Functions | — |
| CLO5 — Arrays/structs/pointers | — |
| CLO6 — Objects / classes | — |
| CLO7 — Test & debug | **D** |
| CLO8 — Communicate & AI use | **D** |

M4 **introduces** CLO3 — selection & iteration begins here. M4 also develops
CLO1, CLO2, CLO7, and CLO8, all already introduced in earlier modules. All
CLOs master at M8's capstone.

---

## Slots pending deep-build authoring

- [ ] Per-MLO "what a student can do" behavioral statement (beyond the
      spine's one-line summary above).
- [ ] Mapping each MLO to the specific Learn/Practice/Apply/Assess artifact
      that measures it. (Assess is stubbed in `_assess-spec.STUB.md`. Learn/
      Practice/Apply are not yet built.)
- [ ] Confirming MLO 4.3's "recover a flowchart from existing code" half.
      The spine names this explicitly ("at least once, the reverse") but
      doesn't say which beat carries it. Candidate: a Practice-beat exit-
      ticket item, or an Assess-tier requirement — see the existing gatekeeper
      lab draft's "flowchart matches code" check, flagged in `_assets.md`.
- [ ] Confirming the boundary between MLO 4.2's "logical operators" and
      MLO 4.1's "switch." A compound condition (`&&`/`||`/`!`) is a natural
      B-tier reach past a C-tier `if`/`else if`/`switch` baseline. Deep-build
      should state explicitly which tier each first appears at, matching the
      Make-gradient's "no trick questions" rule — nothing sprung on students
      that wasn't taught.
