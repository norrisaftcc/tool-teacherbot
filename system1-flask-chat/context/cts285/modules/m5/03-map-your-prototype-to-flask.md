CTS-285 • Module 5

## M5.2 — Map Your Prototype to Flask

You have now tested several responsibility boundaries in a controlled Flask situation. Before you move your own Module 4 prototype, use those findings to decide what should move, what should stay reusable, and what still needs evidence.

Transfer question

**If your text-only prototype already works, which responsibilities should survive the move to Flask unchanged?**

### Bring forward two things

- the carry-forward summary from the Flask Responsibility Lab;
- your Module 4 text-only prototype and the acceptance criterion it demonstrated.

### Map the selected path

Choose the same product-slice path you tested in Module 4. Trace it from user action to response and identify where each responsibility belongs in the Flask version.

**Flask / Interface**

What user input arrives? Which route receives it? What response or template must Flask return?

**Reusable Logic**

Which rule or function from Module 4 should still work without Flask? What input does it need, and what result should it return?

**Data / State**

What information must be retrieved or preserved for the behavior to remain correct across requests?

### Do not migrate assumptions

A working text prototype can still hide choices that become fragile in a web request/response context. Before you code, check for these risks:

- state that exists only because one process stayed open;
- business rules embedded in the text-interface function;
- hard-coded data that the web version will need to retrieve;
- a rule that works only because one interface prevents an invalid action;
- an acceptance criterion you cannot point to in the planned Flask flow.

Workforce habit

**Migrate behavior, not just code.** A framework transition is successful when the tested product rule still behaves correctly, its responsibilities remain understandable, and another developer can see why the structure exists.

### Your next implementation question

Before moving forward, you should be able to state one question your first Flask build must answer. Examples of the form include:

- Can this business rule run unchanged when the input comes from a Flask route?
- What state must persist between two requests for this acceptance criterion to remain true?
- Can Flask present the outcome without owning the decision that produced it?

**Do not submit anything here.** Keep that implementation question with your project. The next activity gives you a controlled Flask application to run and modify before you migrate your own product slice.
