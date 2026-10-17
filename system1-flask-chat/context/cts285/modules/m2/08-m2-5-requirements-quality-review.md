CTS-285 · Module 2.5

## Requirements Quality Review

Before you submit the DataMan Requirements Register, inspect your draft the way a project team would: look for unclear language, unsupported assumptions, hidden design decisions, and requirements that cannot be verified.

Outcome

**MLO 2.3 → CLO 2 — Write Defensible Requirements:** Translate stakeholder and system evidence into clear, testable functional and non-functional requirements.

### Create your working draft first

Before you can review your requirements, you need a working register. In your CTS-285 GitHub repository, create or open:

`docs/requirements.md`

Build your draft with these five sections:

1. **Project Context** — 2–4 sentences identifying the DataMan modernization goal and primary users.
2. **Evidence Notes** — at least four concise evidence statements with the source of each.
3. **Functional Requirements** — at least four requirements numbered FR-01, FR-02, and so on. Include a source/rationale for each.
4. **Non-Functional Requirements** — at least three requirements numbered NFR-01, NFR-02, and so on. Include a source/rationale for each.
5. **Open Questions / Assumptions** — unresolved items that are not yet supported well enough to become confirmed requirements.

**This is your working draft.** Do not submit it yet. Use the quality review below to revise it first. The DataMan Requirements Register assignment that follows this page contains the complete submission requirements and final checklist.

### Use your own draft

Open your current `docs/requirements.md` file in your CTS-285 repository. This page is a quality gate, not a separate graded assignment. Make revisions directly in the project file as you work.

Caution

**Do not wait for the instructor to find every problem.** The purpose of this review is to catch issues while you can still improve the artifact.

### Review every requirement

Work through each check below for every confirmed requirement in your register. If a statement fails a check, revise it before moving on.

#### Clear

**Verify:** Another team member should interpret the statement the same way.

**If it fails:** Replace vague language or split the idea.

#### Supported

**Verify:** The statement connects to manual evidence, elicitation evidence, a stakeholder need, or a confirmed project constraint.

**If it fails:** Add the source or rationale, or move the item to Open Questions / Assumptions.

#### Testable

**Verify:** The team could later determine whether the requirement has been met.

**If it fails:** Clarify the required behavior, condition, or measurable quality.

#### Solution-neutral enough

**Verify:** The requirement does not force a design or technology unless that choice is a real project constraint.

**If it fails:** Rewrite around the needed outcome.

#### Atomic enough

**Verify:** The statement focuses on one main capability or quality.

**If it fails:** Separate unrelated ideas into distinct requirements.

#### Classified correctly

**Verify:** Functional items describe required behavior; non-functional items describe qualities, constraints, or operating conditions.

**If it fails:** Reclassify or rewrite if the statement mixes both.

### Trace one decision backward

Select at least one requirement that changed during the stakeholder simulation or DataMan elicitation case. Confirm that you can trace it backward through the evidence chain:

Evidence

**Evidence → Need → Requirement**

If you cannot explain that chain, the requirement may still be an assumption or a premature solution.

### Final revision check

- At least four functional requirements are present and numbered.
- At least three non-functional requirements are present and numbered.
- Each requirement includes a source or rationale.
- Open questions and assumptions are separated from confirmed requirements.
- Your simulation decision record is saved at `docs/decisions/m2-elicitation-decision-record.md` and used where relevant as evidence.
- Your latest revisions are committed and synced before you submit the register in Canvas.

Your artifact

`docs/requirements.md` — revise this file directly as you complete the quality review.

Analyst rule

**Ready means defensible, not perfect.** You should be able to explain what evidence supports each confirmed requirement and identify what still requires clarification.
