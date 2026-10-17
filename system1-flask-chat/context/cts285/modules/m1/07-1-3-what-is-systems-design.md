CTS-285 · Module 1 · 1.3

## M1.3 — Systems Design

Design begins when the team knows enough about the need to make implementation choices. The goal is to turn validated requirements into a solution another person can understand, evaluate, and eventually build.

Analyst rule

**A requirement says what must be true. A design decision says how the solution will make it true.**

### What design decides

#### Interaction

What the user sees, enters, chooses, and receives.

#### Behavior

What happens, in what order, and under which conditions.

#### Data and state

What information exists, changes, persists, and relates to other information.

#### Responsibility

Which part of the system should own a rule, decision, or operation.

### One requirement can support several design decisions

**Requirement:** The system must give the learner immediate feedback after an answer is submitted.

**Interaction decision:** where and how feedback appears.

**Behavior decision:** what occurs after a correct or incorrect response.

**State decision:** what must be remembered about attempts.

**Responsibility decision:** which layer evaluates correctness and which layer displays the result.

### Good design is traceable

A design choice should exist for a reason. A team should be able to trace it back to a requirement, constraint, risk, or other evidence rather than defending it only as personal preference.

Caution

**Design is not decoration.** A wireframe, diagram, table, prototype, or architecture sketch is useful only when it helps answer a real implementation question.

### Design can change when evidence changes

Design is not a one-time promise. Testing, review, technical constraints, or new evidence may show that an earlier decision needs revision. The professional skill is not avoiding change; it is making the reason for change visible.

****A developer discovers the chosen design makes testing difficult. Is changing it automatically a failure?****

No. If the evidence shows a weak responsibility boundary or other design problem, revising the design is appropriate. The team should record why it changed.

****Can two different designs satisfy the same requirement?****

Yes. Requirements constrain what must be achieved; design evaluates possible ways to achieve it. Evidence and project constraints help the team choose among defensible alternatives.

Outcome

Explain how design turns validated requirements into decisions about interaction, behavior, data/state, and system responsibilities.

**Next:** M1.4 places analysis, design, implementation, and review inside the larger systems development life cycle and shows how different methodologies organize that work.

### Content attribution

Concepts are adapted and summarized from Dennis, A., Wixom, B. H., & Roth, R. M. (2012), *Systems Analysis and Design* (5th ed.), with course-specific examples and instructional framing.
