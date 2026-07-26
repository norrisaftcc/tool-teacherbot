# M8 — Module Learning Objectives (skeleton)

**Status:** skeleton slots only — not authored objectives. Derived from
`_storming/CSC-134-course-spine.md` ("## M8 — Capstone Miniproject") and
`_storming/CSC-134-learning-objectives.md` ("### M8 — Capstone Miniproject").
Deep-build fills in beat-level detail; this file records the MLO shape and
its CLO/CCL wiring so downstream beats (Learn/Practice/Apply/Assess) build
against the same targets.

---

## MLO slots (feeding the CLOs)

| MLO | Statement (from the learning-objectives doc) | Feeds |
|---|---|---|
| **MLO 8.1** | Produce a design document (problem statement, user stories, spec, flowchart) before implementation. | → CLO1 (Design & represent) |
| **MLO 8.2** | Implement, in stages, a working C++ program that meets a self-authored specification. | → CLO2, CLO3, CLO4, CLO5, CLO6 |
| **MLO 8.3** | Test a program against its specification and debug failures across the error taxonomy. | → CLO7 (Test & debug) |
| **MLO 8.4** | Present and defend working software, documenting any AI assistance used. | → CLO8 (Communicate & AI use) |

*Measured by (per the objectives doc):* the capstone (design doc + staged
implementation + presentation). The Assess-beat spec stub
(`_assess-spec.STUB.md`) is where this gets turned into testable acceptance
criteria.

**Note on MLO 8.2's breadth:** unlike every earlier module's MLOs, which each
feed one or two CLOs, MLO 8.2 alone feeds five (CLO2–CLO6). This is the
spine's own design, not scope creep introduced here — M8 is explicitly "the
whole arc, run once, end to end, by you," so its implementation objective
is deliberately the sum of every prior module's core competency.

---

## CCL crosswalk touch (this module)

Per the spine's M8 section: **design, code, test, and debug a C++ program
(summative).** This is the CCL's own closing clause — *"Upon completion,
students should be able to design, code, test, and debug C++ language
programs"* — and M8 is where the spine names it as directly, explicitly
assessed rather than practiced piecemeal.

The CCL crosswalk table (`_storming/CSC-134-course-spine.md`, "CCL crosswalk
(compliance anchor)") also names M8 explicitly for **Object-oriented**
("M7 (struct → class) + M8 (built on classes) — *genuinely covered*") and
for **Design, code, test, debug** ("Whole spine; debugging as curriculum
from M3; M8 summative").

CLO coverage-matrix row for M8 (from the learning-objectives doc's coverage
matrix, I=Introduced / D=Developed / M=Mastered):

| CLO | M8 |
|---|:--:|
| CLO1 — Design & represent | **M** |
| CLO2 — I/O & arithmetic | **M** |
| CLO3 — Selection & iteration | **M** |
| CLO4 — Functions | **M** |
| CLO5 — Arrays/structs/pointers | **M** |
| CLO6 — Objects / classes | **M** |
| CLO7 — Test & debug | **M** |
| CLO8 — Communicate & AI use | **M** |

M8 is the **only** module where every CLO shows **Mastered** — by design,
since the learning-objectives doc states plainly: "every CLO is introduced,
developed across multiple modules, and mastered at the M8 capstone... the
capstone is 'the whole spine, run once, by the student.'" No other module's
row is this uniform; that uniformity is itself the spec for what the
capstone must exercise, not an error to average out.

---

## Slots pending deep-build authoring

- [ ] Per-MLO "what a student can do" behavioral statement (beyond the
      spine's one-line summary above) — especially MLO 8.1, where "produce a
      design document" needs concrete, gradable sub-criteria (what counts as
      a complete problem statement vs. an incomplete one, how many user
      stories, what the flowchart must show).
- [ ] Mapping each MLO to the specific capstone artifact that measures it
      (design doc → MLO 8.1; staged program → MLO 8.2; test/debug log or
      trace → MLO 8.3; presentation/defense → MLO 8.4). Stubbed in
      `_assess-spec.STUB.md`; not yet finalized.
- [ ] Pinning down the spine's own open item on the **AI-permission line**:
      "currently permitted-and-logged on labs; formally owned at the
      capstone (Assess)" (`_storming/CSC-134-course-spine.md`, AI
      collaboration policy section). MLO 8.4 requires documenting AI
      assistance, but the exact ownership boundary ("formally owned" — does
      this mean AI use becomes *unrestricted* at capstone, or *fully
      accountable/disclosed* at capstone?) is named as still open in the
      spine itself and needs a ruling before deep-build writes MLO 8.4's
      acceptance criteria.
- [ ] Confirming what "self-authored specification" (MLO 8.2) means for
      grading consistency across students who will, by definition, each
      build a different program — the rubric-template's tier ladder assumes
      a shared C/B/A/Badge shape; deep-build must define how that shape
      applies when the underlying spec varies student-to-student.
