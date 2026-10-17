CTS-285 • Module 2 Project Evidence

## DataMan Requirements Register

Turn your DataMan evidence and elicitation decisions into the requirements artifact that will feed Module 3 product work.

Outcome

**MLO 2.3 — Write Defensible Requirements:** Translate stakeholder and system evidence into clear, testable functional and non-functional requirements.

**Purpose:** Demonstrate that you can move from evidence → need → requirement without turning assumptions or proposed solutions into confirmed requirements.

### Before you start

Complete the Requirement Repair Lab and M2.5 — Requirements Quality Review. Use your DataMan manual evidence, the elicitation case, and your simulation decision record as source material.

Your simulation record should be saved at:

Your artifact

`docs/decisions/m2-elicitation-decision-record.md`

### Your project artifact

In your CTS-285 GitHub repository, create or update:

Your artifact

`docs/requirements.md`

### Finalize your requirements register

You began **docs/requirements.md** during M2.5. Use the complete template below as a final structure check. Add anything your draft is missing, keep the revisions you made during the quality review, and remove all bracketed prompts or unused placeholder lines before submitting.

**Before submitting:** remove the bracketed prompts and any unused placeholder lines.

**Open the DataMan Requirements Register Template**

**Copy everything inside the box below into docs/requirements.md.**

```
# DataMan Requirements Register

> Replace all bracketed prompts with your own project evidence and requirements. Delete the prompts before submitting.

## Project Context

[In 2–4 sentences, identify the DataMan modernization goal, the primary users, and the problem the project is trying to solve.]

## Evidence Notes

Use at least four concise evidence statements. Label the source of each.

- **E-01 — Source:** [DataMan manual / elicitation case / simulation / other confirmed source]  
  **Evidence:** [What does the source tell you?]

- **E-02 — Source:** [source]  
  **Evidence:** [evidence statement]

- **E-03 — Source:** [source]  
  **Evidence:** [evidence statement]

- **E-04 — Source:** [source]  
  **Evidence:** [evidence statement]

[Add additional evidence notes if needed.]

## Functional Requirements

Write at least four functional requirements. Each requirement should describe a capability or behavior the system must provide.

### FR-01
**Requirement:** The system must [capability/behavior].  
**Source/Rationale:** [Evidence or stakeholder need that supports this requirement.]

### FR-02
**Requirement:** The system must [capability/behavior].  
**Source/Rationale:** [Evidence or stakeholder need that supports this requirement.]

### FR-03
**Requirement:** The system must [capability/behavior].  
**Source/Rationale:** [Evidence or stakeholder need that supports this requirement.]

### FR-04
**Requirement:** The system must [capability/behavior].  
**Source/Rationale:** [Evidence or stakeholder need that supports this requirement.]

[Add additional functional requirements if needed.]

## Non-Functional Requirements

Write at least three non-functional requirements. Each requirement should describe a measurable quality, constraint, or condition the system must satisfy.

### NFR-01
**Requirement:** The system must [measurable quality/constraint/condition].  
**Source/Rationale:** [Evidence or project constraint that supports this requirement.]

### NFR-02
**Requirement:** The system must [measurable quality/constraint/condition].  
**Source/Rationale:** [Evidence or project constraint that supports this requirement.]

### NFR-03
**Requirement:** The system must [measurable quality/constraint/condition].  
**Source/Rationale:** [Evidence or project constraint that supports this requirement.]

[Add additional non-functional requirements if needed.]

## Open Questions / Assumptions

Do not turn an unsupported idea into a confirmed requirement. Record unresolved items here until evidence supports a decision.

- **Q-01:** [What still needs to be clarified or confirmed?]
- **Q-02:** [What still needs to be clarified or confirmed?]

[Add or remove items as appropriate.]

## Final Quality Check

Before submitting, confirm that each requirement is:

- [ ] Clear enough for another team member to interpret consistently.
- [ ] Supported by evidence, a stakeholder need, or a confirmed project constraint.
- [ ] Testable or verifiable later.
- [ ] Solution-neutral enough for this stage of the project.
- [ ] Focused on one main capability or quality.
- [ ] Classified correctly as functional or non-functional.

Also confirm:

- [ ] At least four functional requirements are included.
- [ ] At least three non-functional requirements are included.
- [ ] Every confirmed requirement has a source/rationale.
- [ ] Open questions and assumptions are separated from confirmed requirements.
- [ ] The simulation decision record is saved at `docs/decisions/m2-elicitation-decision-record.md`.
- [ ] This file is saved as `docs/requirements.md`, committed, and synced to GitHub.
```

### Required structure

Section | What to Include

**Project Context** | 2–4 sentences identifying the modernization goal and primary users.

**Evidence Notes** | At least four concise evidence statements from the DataMan manual, elicitation case, simulation, and/or other confirmed project evidence. Label the source of each.

**Functional Requirements** | At least four clear functional requirements numbered FR-01, FR-02, and so on.

**Non-Functional Requirements** | At least three clear non-functional requirements numbered NFR-01, NFR-02, and so on.

**Open Questions / Assumptions** | List unresolved items that are not yet supported well enough to become confirmed requirements.

### Trace each requirement to evidence

For every FR and NFR, include a short source/rationale. A full traceability matrix comes later; for now, show enough evidence that another team member can understand why the requirement exists.

**FR-01:** The system must allow a learner to submit an answer to a math problem and receive correctness feedback.

**Source/Rationale:** Original DataMan Answer Checker behavior + learner need for immediate practice feedback.

### Professional quality standard

Each confirmed requirement should be:

- **Clear** — another team member can interpret it consistently.
- **Grounded** — supported by evidence, a stakeholder need, or a confirmed project constraint.
- **Testable** — the team can later determine whether it was satisfied.
- **Solution-neutral enough** — it does not force a design or technology unless that choice is truly constrained.
- **Focused** — it addresses one main capability or quality.
- **Correctly classified** — functional, non-functional, or unresolved.

Caution

**Do not invent evidence to make a requirement look complete.** If the team does not yet know enough to defend an item, place it under Open Questions / Assumptions.

### GitHub Workflow

1. Open your existing CTS-285 repository or Codespace.
2. Open the **docs** folder.
3. Create **requirements.md** if it does not already exist.
4. Copy the template from this assignment into the file.
5. Replace the bracketed prompts with your own DataMan evidence and requirements.
6. Use your simulation decision record and other Module 2 evidence while drafting.
7. Complete M2.5 — Requirements Quality Review and revise the file.
8. Remove unused prompts/placeholders and preview the Markdown for readability.
9. Commit with a message that describes the project change.
10. Sync the repository.
11. Open **docs/requirements.md** on GitHub and copy its direct URL.

**Commit-message example:** refine DataMan requirements from elicitation evidence

### Submit in Canvas

Submit the direct GitHub URL to your final **docs/requirements.md** file. Do not upload a duplicate copy of the Markdown file to Canvas.

### How It Will Be Evaluated

The Canvas rubric evaluates evidence and traceability, requirement quality, classification and separation of uncertainty, and professional GitHub artifact quality. The assignment is worth **20 points**.

### This Carries Forward

In Module 3, approved requirements become user stories, acceptance criteria, estimates, and prioritized backlog work. The stronger this register is, the stronger the product work built from it will be.
