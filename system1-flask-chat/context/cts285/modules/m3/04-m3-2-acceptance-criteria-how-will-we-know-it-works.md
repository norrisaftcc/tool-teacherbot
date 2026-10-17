CTS-285 • Module 3 • M3.2

## Acceptance Criteria: How Will We Know It Works?

A user story explains who needs something and why it matters. Acceptance criteria define the observable conditions that must be true before the team can say the story has been satisfied.

Analyst rule

**A story gives direction. Criteria make success testable.** Without acceptance criteria, two people can read the same story and imagine different results. Good criteria reduce that ambiguity by describing behavior the team can observe, test, and discuss before implementation begins.

### Story versus acceptance criteria

#### User Story

**Example:** As a learner, I want another attempt after an incorrect answer so that I can correct my work without immediately being given the answer.

**Purpose:** identifies the user, need, and value.

#### Acceptance Criteria

- After an incorrect answer, the learner is offered another attempt.
- The correct answer is not shown immediately after the first incorrect attempt.
- The learner can submit another response to the same problem.

### What strong acceptance criteria do

#### Observable

Someone can see or verify whether the condition occurred.

#### Specific

The condition is precise enough to guide discussion and testing.

#### Testable

The team can determine whether the condition passes or fails.

#### Relevant

The criterion supports the story and its underlying requirement instead of adding unrelated scope.

Analyst rule

**Acceptance criteria are not a design specification.** Criteria should define the behavior or result that must be true. They should not automatically decide the button color, database structure, framework, page layout, or other implementation details unless a validated requirement genuinely makes that detail necessary.

### Given / When / Then

One useful way to write behavioral acceptance criteria is the **Given / When / Then** pattern:

**Given** describes the starting condition or context.

**When** describes the action or event.

**Then** describes the observable result that should follow.

#### Example

**Story:** As a learner, I want another attempt after an incorrect answer so that I can correct my work without immediately being given the answer.

**Given** a learner is answering a practice problem,

**When** the learner submits an incorrect answer,

**Then** the system allows another attempt without immediately revealing the correct answer.

### The pattern helps, but the reasoning matters more.

Not every acceptance criterion must be written as Given / When / Then. A concise checklist can also work when the behavior is already clear. The goal is not to force every condition into a template. The goal is to make success observable and testable.

**Weak criterion: “The retry feature works correctly.”**

**Problem:** “Works correctly” does not define what anyone should observe.

**Repair:** State the behavior that must occur, such as allowing another attempt after an incorrect response without immediately displaying the answer.

**Weak criterion: “The Retry button is blue and 140 pixels wide.”**

**Problem:** This specifies interface design rather than the required behavior unless those exact design details are supported by a validated requirement.

**Repair:** Describe what the learner must be able to do and what result must follow.

**Weak criterion: “Learners enjoy using the retry feature.”**

**Problem:** Enjoyment is not directly established by whether the feature behaves as required.

**Repair:** Define an observable system behavior. User satisfaction may matter, but it requires different evidence than a functional acceptance check.

### Acceptance criteria protect traceability

As the product moves from analysis toward implementation, the chain should remain visible:

**Requirement**

**User Story**

**Acceptance Criteria**

**Later Test Evidence**

This matters later. When the team begins implementation, acceptance criteria help determine what must be tested and whether the built behavior actually satisfies the product work.

Analyst rule

**Before you move on.** For each criterion, ask: **Could another person observe the system and determine whether this condition passed or failed?** In the next lab, you will diagnose and repair acceptance criteria before using them in your own backlog.
