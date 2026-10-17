CTS-285 • Module 5 • 12 Points

## Extend Your Flask Application with a DataMan Feature

Your minimal Flask application proved that one product slice could survive the move into a web framework. Now grow that application by implementing one connected DataMan story or feature and evaluating what the added behavior changes.

### Extension question

**What changes when one working Flask slice has to support another real product behavior without losing traceability or understandable boundaries?**

### Choose one connected story

Select one DataMan story or feature that is already supported by your earlier requirements, backlog, design evidence, or acceptance criteria. It should connect meaningfully to the Flask work you already completed.

**Keep the extension small enough to test end to end.**

Do not add unrelated features, redesign the whole application, or introduce a new technology simply because the feature could eventually use it.

### Before you code

Identify the evidence that defines the feature:

- the requirement, story, or product need it addresses;
- the acceptance criterion or observable behavior that will tell you it works;
- the existing business logic you can reuse;
- the route/interface change the feature requires;
- the state or data the feature must read, change, or preserve;
- one uncertainty or implementation question you expect to test.

### Build one vertical slice

Implement the feature through the full path needed to exercise it:

**User Action**
input or trigger

**Flask**
route + coordination

**Logic**
product rule

**State / Data**
read or preserve

**Response**
observable result

If the selected story depends on persistence beyond the mechanism currently supported in this module, do not add an unsupported database just to complete the assignment. Implement the behavior at the supported state/data boundary and record the persistence dependency as an unresolved implementation need.

### Test the feature and the application around it

Verify the new feature against its acceptance criterion. Then rerun at least one behavior that already worked before the extension.

You are looking for two different kinds of evidence:

- **feature evidence:** does the new story behave as expected?
- **change-impact evidence:** did the extension weaken or alter behavior that previously worked?

### Classify what you find

If the implementation or test result does not match what you expected, determine whether the issue is primarily:

- a coding defect;
- a weak responsibility boundary;
- a state/data problem;
- a design decision that now needs revision;
- or a source ambiguity that requires a documented question.

Revise the code, design evidence, or project record when the evidence warrants it.

### Record the implementation decision

In your repository, add a concise note that records:

- the story/feature you implemented;
- the acceptance criterion you tested;
- what changed in the Flask, business-logic, and state/data responsibilities;
- one meaningful test result or consequence;
- what you kept, revised, deferred, or turned into a next question.

Analyst rule

**Question → Implementation/Evidence → Decision → Test Result → Evaluation → Revision → Next Question**

### Leave a reviewable Git history

Use the Git/GitHub workflow already established for this course. Your repository history should make it possible to see the feature grow through meaningful changes rather than one unexplained final commit.

### Submit in Canvas

Submit the **direct GitHub URL** to the Module 5 Flask implementation containing the completed feature.

The instructor should be able to locate:

- the implemented DataMan story/feature;
- traceability to its requirement/story and acceptance criterion;
- the relevant Flask, business-logic, and state/data changes;
- feature and change-impact test evidence;
- the implementation decision note;
- meaningful Git history.

**Do not upload duplicate code files to Canvas.** GitHub remains the source of truth for the implementation.

Analyst rule

**Every feature changes a system, not just a file.** Check what the new behavior needs, what it touches, what it might break, and what evidence should change with it.
