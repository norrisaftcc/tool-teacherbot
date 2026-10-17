CTS-285 • Module 4

## M4.1 — Design for Implementation

A design artifact is useful when it helps answer a question that matters before implementation. The goal is not to collect diagrams. The goal is to reduce uncertainty enough to make a sound decision.

Analyst rule

**Start with the question, not the tool.** If you cannot explain what you are trying to understand, a diagram may only make the uncertainty look organized.

### What kind of question are you trying to answer?

Most implementation questions fall into a few useful families. A single product slice may raise more than one.

#### Interaction

What does the user need to see, enter, choose, or receive?

Useful evidence might include a wireframe, annotated screen sketch, or user-flow sketch.

#### Behavior

What must happen, in what order, and under which conditions?

Useful evidence might include a flow, state model, sequence sketch, pseudocode, or executable spike.

#### Data and state

What information must exist, persist, change, or relate to something else?

Useful evidence might include an ERD, relationship sketch, field list, or state table.

#### Architecture

Which responsibility belongs where, and what should stay independent?

Useful evidence might include a layer/component sketch, class relationship, interface contract, or prototype structure.

#### Dependency and constraint

What must be available, true, completed, or decided before this work can proceed?

Useful evidence might include a dependency map, constraint list, spike result, or ADR.

#### Readiness

Do we know enough to build this slice responsibly?

Useful evidence comes from the other questions: acceptance criteria, design evidence, prototype behavior, dependencies, and unresolved uncertainty.

### Two modelling views you need to know

Before you choose a design artifact, you need enough notation knowledge to recognize what different models can show. In CTS-285, two small modelling views are sufficient for the questions this project asks.

#### Behavior over time: UML sequence view

Use a sequence view when the important question is *who or what interacts, and in what order?*

- Place the participating user, interface, logic, or data responsibility across the top.
- Read time from top to bottom.
- Use arrows to show messages, calls, requests, or returned results.
- Include only interactions needed to answer the design question.

#### Structure and data: class relationship or ERD view

Use a structure/data view when the important question is *what information exists, what owns it, and how do the parts relate?*

- Name the important entity or class-like concepts.
- Record only the fields or responsibilities needed for the question.
- Draw relationships so another person can see what connects to what.
- For persistent data, make one-to-one, one-to-many, or many-to-many relationships explicit when they matter.

Analyst rule

**Use Mermaid for the course modelling views.** GitHub can keep the text source beside the rest of the project evidence. If you need a drag-and-drop alternative, use diagrams.net through its VS Code extension and keep the editable source with the project. The tool does not decide what the model means; your design question and source evidence do.

### Worked DataMan pair

Use the same product evidence to see what the two views answer differently.

#### Behavior over time: two-attempt answer flow

Question: *What happens from the learner's first answer through the second miss?*

```
sequenceDiagram
  actor Learner
  participant UI
  participant Checker
  Learner->>UI: submit answer
  UI->>Checker: check answer
  Checker-->>UI: incorrect, attempt 1
  Learner->>UI: submit second answer
  UI->>Checker: check answer
  Checker-->>UI: incorrect, reveal correct answer
```

This view makes order and responsibility visible. It does not tell you how attempt data should be stored.

#### Structure and state: attempt tracking

Question: *What information must exist so the system can enforce the two-attempt behavior?*

```
classDiagram
  class PracticeSession {
    attemptCount
    currentProblem
    answerStatus
  }
  class Problem {
    prompt
    correctAnswer
  }
  PracticeSession --> Problem : tracks
```

This view makes state ownership visible. It does not show the exact order of the learner interaction.

**Try it — ungraded.** Choose one of the situations below. Before opening its reveal, sketch either a small Mermaid sequence view or a small class/ERD-style view that answers one design question. Keep only the elements needed to answer that question. Nothing is submitted for this try.

### Choose the lightest evidence that can answer the question

More documentation does not automatically mean better design. Use enough detail to support a decision, reveal a problem, or communicate something another person needs to act on.

**Example:** A DataMan story says a learner gets two attempts before the correct answer is revealed.

- **If the uncertainty is screen behavior:** sketch the interaction states.
- **If the uncertainty is the order of events:** model the behavior or sequence.
- **If the uncertainty is where attempt count lives:** inspect state/data responsibilities.
- **If the uncertainty is whether the design works at all:** test it in a small prototype.

Analyst rule

**The same story can create different design questions.** That is not a problem. What matters is whether the question is relevant to implementation and whether the evidence you choose can actually help answer it.

### Try the question before the artifact

For each situation below, decide what you would need to understand **before** opening the reveal. There may be more than one defensible path.

**Situation 1: A curator can load up to 10 problems into a Memory Bank set.**

**Useful questions might include:** Where is the 10-problem limit enforced? What happens when an eleventh problem is attempted? Does the interface prevent it, does the business logic reject it, or both? What state must be stored?

**Possible evidence:** relationship/data sketch, behavior flow, acceptance-criteria trace, or a small prototype test. An ERD might help if the uncertainty is relationship/persistence; it would not answer the whole behavior question by itself.

**Situation 2: A learner gets one wrong answer, tries again, then sees the correct result after a second miss.**

**Useful questions might include:** What states exist after each attempt? Which layer owns the attempt count? What must the user see after try one versus try two? When is the result recorded?

**Possible evidence:** state/flow representation, sequence sketch, pseudocode, acceptance-criteria trace, or text-prototype behavior.

**Situation 3: A curator needs to review a learner's results later without having watched the session.**

**Useful questions might include:** What must persist after the session ends? Which result belongs to which learner, problem, or practice set? What does the curator actually need to see?

**Possible evidence:** ERD/relationship sketch, result-state model, wireframe, or a trace from the story and acceptance criteria into the planned data.

**Situation 4: Two students design the same DataMan feature differently, and both designs appear to satisfy the acceptance criteria.**

**Useful questions might include:** Does the source evidence settle the difference? Does one design create a downstream constraint the other avoids? Is the difference important enough to record as an architectural decision?

**Possible evidence:** manual/source comparison, prototype result, tradeoff table, dependency check, ADR, or peer review. Difference does not automatically mean error.

### A useful design decision has a trace

**Product Work**

**Question**

**Evidence**

**Decision**

**Test / Review**

**Revise or Proceed**

A strong decision can be explained backward: *We made this choice because this question mattered, this evidence informed it, and this test or review either supported it or caused us to change it.*

### Before you move on

Open your Module 3 product backlog and identify one story or small story set you expect to carry forward. Do not choose a diagram yet. First ask: **What is still unclear enough that coding this now would create avoidable risk?**

**Next:** In the DataMan Design Investigation, you will use that question to decide what evidence is worth creating.
