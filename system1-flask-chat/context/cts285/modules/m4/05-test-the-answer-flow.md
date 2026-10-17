MODULE 4 · TEST THE DESIGN

## Test the Answer Flow

You have framed an implementation question for your own DataMan product work. Before you investigate that product slice further, you will work through a controlled problem where the consequences of design choices are easier to see.

**Your job is not to predict the correct configuration.** Configure the system, operate it, inspect what happens, and revise when the evidence shows that a decision is weak.

### The system requirement

DataMan allows exactly two answer attempts. After the first miss, the correct answer stays hidden and a second try is allowed. After the second miss, the correct answer is revealed. Later, a curator must be able to distinguish first-try success, second-try success, and two misses.

### What you are testing

- **Behavior:** does the two-attempt flow actually work across each required outcome?
- **State:** what must the system know after the first attempt and after an interruption?
- **Responsibility:** which rules belong in reusable business logic instead of one interface?
- **Persistence:** what evidence has to survive so later reporting is possible?

### Answer Flow Lab

Open the lab in a new tab. Configure a design, run the available learner scenarios, inspect the consequences, and revise as needed.

[Open the Answer Flow Lab](https://amlw05.github.io/cts-285-course-simulations/m4/answer-flow-lab/)

### Bring back evidence, not a score

Nothing from the lab is submitted yet. When you return to Canvas, be ready to identify:

- one failure or near-failure your configuration exposed;
- the design decision you changed;
- what consequence changed after the revision;
- one principle that should carry into a different interface or implementation.

**Workforce connection:** implementation is often where hidden assumptions become visible. Strong analysts and developers use those failures as evidence, revise the design, and preserve the reasoning that should guide the next build decision.

**Nothing is due here.** After completing the lab, return to this Canvas tab and use **Next** to continue.
