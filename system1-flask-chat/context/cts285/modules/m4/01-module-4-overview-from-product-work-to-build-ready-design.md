CTS-285 • Module 4

## From Product Work to Build-Ready Design

In Module 3, you decided what product work should move forward. In Module 4, the question changes: **What still needs to be asked, seen, tested, or resolved before that work is safe and clear enough to build?**

Analyst rule

**The project does not reset here.** Your `docs/product-backlog.md`, requirement traceability, acceptance criteria, and DataMan evidence become the starting point for design. You are not beginning a new project. You are testing whether the work you already selected is actually ready to implement.

### The handoff

**M2**
What must the system do?

**M3**
What product work should move forward?

**M4**
What makes that work safe and clear enough to build?

**M5**
Build and test the first Flask implementation.

### How your work changes in this module

You will get less step-by-step direction than you did earlier in the course. Instead of being told which artifact to create first, you will increasingly decide **what question needs to be answered** and **what evidence would help answer it**.

**Your design loop:**

**Question** → Evidence → Decision → Consequence → Evaluation → Revision → **Next Question**

Different students may ask different useful questions and make different defensible decisions. The goal is not to match one hidden design. The goal is to make decisions you can explain, test, and revise.

### Module Learning Outcomes

By the end of this module, you will be able to:

**MLO 4.1 → CLO 3**

#### Frame Design Questions and Select Evidence

Identify an implementation-relevant question and choose or create evidence that can help answer it.

**MLO 4.2 → CLO 3, CLO 4**

#### Develop and Test Implementation-Supporting Design

Create useful design evidence and a minimal three-layer text prototype that test selected DataMan decisions.

**MLO 4.3 → CLO 3, CLO 4**

#### Evaluate and Revise Build Readiness

Use design evidence, prototype behavior, acceptance criteria, dependencies, and uncertainty to decide whether work should proceed, change, split, or wait.

### What counts as design evidence?

A design artifact is useful only when it answers a real question. In this module you will learn two compact modelling approaches you can use when the question calls for them: a **sequence view** for behavior over time and a **structure/data view** using a class relationship or ERD-style model. Depending on the work you select, other evidence may still include a wireframe, interaction sketch, flow, architecture sketch, dependency map, ADR, technical spike, or working prototype behavior.

Analyst rule

**You are not collecting diagrams.** Start with the question. Use the simplest evidence that helps you make a better decision.

### What you will do

1. Select a product slice from your Module 3 backlog.
2. Identify what is still unclear enough to make implementation risky.
3. Choose and create only the design evidence needed to answer those questions.
4. Compare your analysis with others and revise when new evidence changes the decision.
5. Design and build a three-layer text-only DataMan prototype in Python.
6. Use prototype behavior to expose missing assumptions, state, dependencies, or design problems.
7. Make a build-readiness judgment and prepare the work that will move into Flask in Module 5.

**What carries forward from Module 3?**

Bring forward your `docs/product-backlog.md`, the requirement and story traceability behind the work you select, its acceptance criteria, and any unresolved dependencies or questions already identified.

A story that was prioritized in Module 3 is not automatically ready to code. Module 4 is where you test that assumption.

**What is the text-only prototype?**

You will build a small DataMan prototype with the same basic separation the later application will use:

- **Text interface layer** — menus and input/output.
- **Business-logic layer** — the Python code that performs DataMan behavior independently of the interface.
- **Stubbed data layer** — a simple stand-in for persistence.

This is not a throwaway side project. The goal is to learn from the architecture now and reuse as much of the business logic as practical when Flask is introduced in Module 5.

**What will you leave in GitHub?**

Your persistent M4 evidence will include your prototype code, any design evidence or decision records that actually support implementation, and a build-readiness package in:

`docs/design/build-readiness-package.md`

That package will show the questions you pursued, the evidence you used, the decisions and revisions you made, what the prototype revealed, and whether the selected work is Ready, Revise, Split, or Blocked.

Working principle

**Keep the design as simple as the evidence allows.** Make your reasoning visible, get feedback early, and change course when the evidence tells you to.

**Next:** You will begin with the difference between creating a design artifact because it was assigned and creating one because it answers a question your implementation actually needs resolved.
