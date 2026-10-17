CTS-285 • Module 5 • 12 Points

## Build Your Minimal Flask Application

Move the same product slice you tested in Module 4 into Flask. Your goal is not to add more features. Your goal is to prove that the behavior still works when the interface changes and that the responsibility boundaries remain understandable.

Implementation question

**Can the product behavior you already designed and tested survive the move into Flask without losing traceability, reusable logic, or a clear state/data boundary?**

### Build from your existing evidence

Use the same product slice, business logic, and acceptance criterion you carried forward from Module 4. Reuse sound work when it still fits. Revise it only when the Flask implementation gives you a reason.

### Your minimal Flask application must show

- a working Flask application that runs in Codespaces;
- at least one route/request-response path for the selected product slice;
- business logic that remains reasonably separate from Flask-specific route code;
- a deliberate data/state boundary appropriate for this stage of the project;
- one complete user path that exercises the selected behavior;
- evidence that at least one related acceptance criterion was tested against the working Flask implementation;
- meaningful Git commits that make the implementation history understandable.

**Keep the scope narrow.**

This is not the assignment where you build the full DataMan application. Implement only enough Flask structure to prove that the selected slice works and that your Module 4 decisions hold up in the new environment.

### Test the transition

Run the selected path in Flask and compare the observed behavior with the acceptance criterion you carried forward. If the behavior differs, decide whether you found:

- a coding defect;
- a weak implementation choice;
- a design assumption that no longer holds;
- a state/data problem;
- or an unresolved source question.

Revise the implementation or project evidence when the new evidence warrants it.

### Record one implementation finding

Your artifact

`docs/decisions/m5-implementation-finding.md` — record what the Flask implementation confirmed, exposed, or forced you to reconsider.

Your finding should point to actual implementation or test evidence. A statement such as “Flask was harder than I expected” is not enough.

### Submit in Canvas

Submit the **direct GitHub URL** to the Module 5 Flask implementation in your CTS-285 repository.

The instructor should be able to locate:

- the Flask entry point and route structure;
- the reusable business logic for the selected product slice;
- the data/state boundary used by that behavior;
- the acceptance criterion or traceability evidence you tested;
- the implementation finding;
- the relevant commit history.

**Do not upload duplicate code files to Canvas.** GitHub remains the source of truth for the implementation.

Workforce habit

**Preserve what works. Change what the evidence says must change.** Framework migration is not successful because the page loads; it is successful when the behavior, boundaries, and reasoning still make sense.
