MODULE 4 · DESIGN VALIDATION · 12 POINTS

## Design and Test a Text-Only Prototype

Use the design decision you developed in the Module 4 investigation to create a minimal text-only prototype. The goal is not to build the finished application. The goal is to test whether your design decisions hold up when they must actually run.

**Keep the scope small.** Build one complete product-slice path well enough to test behavior, state, data responsibility, and separation of concerns. Flask and the first framework-based application begin in Module 5.

### Required structure

Your prototype must contain three distinguishable layers:

1. **Text interface layer** — receives input and displays output.
2. **Business logic layer** — contains reusable rules and decisions that do not depend on one interface.
3. **Stubbed data layer** — provides or preserves only the data/state needed to test the selected product slice without requiring the final database implementation.

### Build from the evidence you already created

Use your investigation brief, Lab Evidence Record, Design Studio work, requirements, backlog evidence, and acceptance criteria. Your prototype should test the design question you carried forward rather than start a new feature from scratch.

If running the prototype exposes a contradiction, missing state, weak assumption, or misplaced responsibility, revise the design or record the unresolved issue. That discovery is part of the work.

### Minimum prototype evidence

- One complete path through the selected product slice runs from the text interface.
- The business rule or rules for that path can operate independently of the interface.
- The data boundary is stubbed or replaceable rather than hard-coded throughout the interface.
- State required by the selected behavior is represented deliberately.
- At least one acceptance criterion can be demonstrated through the prototype.
- README notes or code comments identify intentionally stubbed work, unresolved uncertainty, and any revision caused by testing the prototype.

**What carries into Module 5:** sound business logic, the selected product slice, acceptance criteria, known state/data needs, and unresolved implementation questions. You should not rebuild good logic simply because the interface changes to Flask.

### Submit in Canvas

Submit the **direct GitHub URL** to the prototype location in your CTS-285 repository. The instructor should be able to locate:

- the text interface entry point;
- the business logic;
- the stubbed data layer;
- the related design-investigation record or notes that explain what the prototype tested.

Do not upload duplicate code files to Canvas. GitHub remains the source of truth for the prototype.
