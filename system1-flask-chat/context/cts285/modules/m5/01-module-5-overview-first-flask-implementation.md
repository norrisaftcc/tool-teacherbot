CTS-285 • Module 5

## First Flask Implementation

In Module 4, you tested whether a selected product slice was clear enough to implement. In Module 5, that work moves into a framework: **How do you turn tested business logic into a small working Flask system without losing the decisions, traceability, and separation that made the design defensible?**

Developer rule

**The project does not reset when the framework changes.** Reuse sound business logic, requirements, acceptance criteria, design evidence, and known state/data needs. Change them only when implementation evidence gives you a reason.

### The handoff

**M3**
What product work should move forward?

**M4**
What makes that work safe and clear enough to build?

**M5**
How do we preserve sound decisions while moving into Flask?

**Next**
Grow, test, review, and improve the working system.

### How your work changes in this module

You are no longer testing the design only through representations and a text interface. Flask introduces routes, requests, responses, templates, and framework conventions. Your job is to learn what belongs to the framework, what should remain reusable business logic, and what implementation evidence says about the decisions you carried forward.

**Your implementation loop:**

**Question** → Implementation/Evidence → Decision → Test Result → Evaluation → Revision → **Next Question**

Different students may make different defensible implementation choices when the evidence allows them. What matters is whether the application works, the reasoning is traceable, the responsibilities remain understandable, and new evidence leads to appropriate revision.

### Module Learning Outcomes

By the end of this module, you will be able to:

**MLO 5.1 → CLO 4**

#### Distinguish Framework and Core Responsibilities

Differentiate Flask interface/request-response responsibilities from reusable business logic and data/state responsibilities.

**MLO 5.2 → CLO 4**

#### Build a Minimal Flask Implementation

Create and run a small Flask application that carries forward a selected DataMan product slice and appropriate reusable logic.

**MLO 5.3 → CLO 4**

#### Test, Evaluate, and Revise

Test working behavior against acceptance criteria and use implementation evidence to revise code, design, or product decisions when warranted.

### What you will do

1. Examine the boundary between Flask responsibilities and reusable application logic.
2. Work through controlled Flask examples before modifying your own project.
3. Run, inspect, and make targeted changes in the course development environment.
4. Move one tested product slice from the M4 text prototype into a minimal Flask structure.
5. Verify the migrated behavior against its acceptance criteria.
6. Add or refine one DataMan feature as a vertical slice without scattering its rules across the framework.
7. Use test results, code behavior, review, and source evidence to decide what should be kept, revised, or investigated next.

**What carries forward from Module 4?**

Bring forward the selected product slice, acceptance criteria, reusable business logic from the text-only prototype, identified state/data needs, design evidence that still holds, and unresolved implementation questions.

If your M4 prototype exposed a problem, carry that problem forward too. Uncertainty is evidence when it is made visible and investigated.

**What changes when Flask enters the system?**

Flask adds a web framework layer: routes receive requests, templates present responses, and framework conventions organize the application. Those responsibilities should not automatically absorb business rules that already work independently.

One of the central questions in this module is therefore not simply “How do I write this in Flask?” but “What should Flask own, and what should remain reusable outside Flask?”

**What evidence matters in Module 5?**

Useful evidence includes running application behavior, acceptance-criteria tests, targeted code changes, Git/GitHub history, review findings, and concise records of implementation decisions or unresolved questions.

Canvas will capture meaningful academic submissions and checkpoints; GitHub remains the persistent source for code and technical evidence. You should not duplicate the same artifact in multiple places without a reason.

Workforce principle

**Frameworks change. Responsibilities, traceability, and evidence still matter.** Build so another developer can understand what the framework is doing, what the application is deciding, and why the behavior is correct.

**Next:** You will examine a small Flask request from the outside in and decide which parts belong to the framework, the business logic, and the data boundary before you write or move project code.
