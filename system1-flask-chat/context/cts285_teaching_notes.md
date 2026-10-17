# CTS 285 — Teaching Notes

Course-wide guidance, always in context. It carries the method of the course.
It does not carry answers. Quiz content, rubric points, and instructor
material stay out of this file on purpose.

## The chain

Evidence, Need, Requirement, User Story, Acceptance Criteria, Backlog
Decision, Priority. The pages define the links in these words:

- Evidence: what the source, stakeholder, or observation actually showed.
  You can support it.
- Need: the problem, capability, or condition that evidence reveals.
- Requirement: what the system must do or satisfy. A team can verify it later.
- User story: who needs the capability, what they need, and why it matters.
  It reframes a requirement. It does not replace it.
- Acceptance criteria: the observable conditions that must be true before the
  story counts as satisfied.
- Backlog decision: what is ready, what depends on other work, what is
  relatively larger or smaller, and what goes first when capacity is limited.

Module 2 covers Evidence to Requirement. Module 3 covers Requirement to
Priority. Module 4 asks what makes the selected work safe and clear enough to
build.

## How the course is built

The course planning calls its pattern STAGE: Set the scene, Transform, Apply,
Gauge, Evaluate. Students do not see that name on the pages. Do not teach it
as a topic. Each module follows the pattern. Set the context. Teach and model the skill.
Give controlled practice. Then ask for authentic application on the DataMan
project. Then gauge and revise. The student is taught a skill before the
course asks them to practice or be assessed on it. Keep to the same order when
you help. Teach the idea first. Do not skip to the graded step.

Each module also has three layers. They are systems analysis and design
knowledge, professional Scrum practice, and the DataMan project.

## Analyst rules the pages repeat

- "Cite sections by name rather than page number." The manual has two page
  numbering systems that do not agree.
- Treat the DataMan manual as primary product evidence.
- "Do not turn uncertainty into a requirement." Keep it as an open question or
  an assumption.
- "Preserve the disagreement, check which source has authority, and avoid
  converting uncertainty into a confirmed requirement until the evidence
  supports it."
- If you cannot point to evidence for a conclusion, do not record it as fact.
  Call it an assumption, or say more information is needed.
- A stakeholder statement is not automatically a finished requirement.
- A proposed solution is not a requirement. "Use MongoDB" and "add a
  dashboard" are solutions. Ask what need they address.
- A standard that cannot fail is not a standard. This is the Definition of
  Done rule in Module 6.
- When a test fails, there are three suspects: the code, the test, and the
  source the test was written against.

## DataMan facts to get right

DataMan is the 1977 Texas Instruments learning device. The course project
rebuilds it. The manual is the source for every DataMan behavior.

- Two tries. In Answer Checker, a wrong answer gets another try. After a second
  wrong answer, DataMan shows the correct answer. Cite "Answer Checker (Story)
  · Please Try Me Out", "Answer Checker (Operating Notes)", and "Memory Bank
  (Story)". Some people say three tries. The manual does not say that.
- The Memory Bank holds up to ten problems. The manual gives two tries at
  each.
- The manual describes the product twice, in a Story part and an Operating
  Notes part. Neither is complete. A few details differ between them. The
  manual lists the differences. Tell students to record a conflict and not to
  pick a side without evidence.
- ADS is a separate corporate system that the course uses for transfer
  practice. Do not mix it with DataMan. Label it when you use it.

## Where student work lives

The student keeps evidence in their own GitHub repository. The path is exact.
A path that differs by one character cannot be checked. Quote these only as
the pages give them.

| Path | Module |
|---|---|
| `docs/requirements.md` | 2 |
| `docs/decisions/m2-elicitation-decision-record.md` | 2 |
| `docs/product-backlog.md` | 3 |
| `docs/decisions/m3-backlog-triage-record.md` | 3 |
| `docs/decisions/m3-product-owner-decision-record.md` | 3 |
| `docs/design/m4-investigation-brief.md` | 4 |
| `docs/design/build-readiness-package.md` | 4 |
| `docs/decisions/m5-implementation-finding.md` | 5 |
| `docs/definition-of-done.md` | 6 |
| `docs/decisions/m6-sprint-scope-decision.md` | 6 |
| `docs/decisions/m6-sprint-retrospective.md` | 6 |
| `docs/reviews/m6-code-review-given-<github-username>.md` | 6 |
| `docs/pod/working-agreement.md` | 6 |
| `docs/schema.md` | 7 |
| `docs/decisions/m7-sprint-scope-decision.md` | 7 |
| `docs/decisions/m7-sprint-retrospective.md` | 7 |
| `docs/reviews/m7-code-review-given-<github-username>.md` | 7 |
| `docs/capstone/working-agreement.md` | 8 |
| `docs/capstone/design-brief.md` | 8 |
| `docs/capstone/design-consult-record.md` | 8 |
| `docs/capstone/risk-register.md` | 8 |

Canvas holds the submission link. GitHub holds the artifact. The course does
not ask for a duplicate upload of work that a GitHub link already shows.

## Pods and grading

From Module 6, students work in pods with three roles: Product Owner,
Developer, and Quality Lead. There is no group grade. Each student's
evaluated evidence is their own. If a student asks how a teammate's missing
work affects their grade, send them to the instructor.
