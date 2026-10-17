CTS-285 · Module 7 Sprint Planning

## Sprint 2 Planning — Change the System, Bound the Increment

Sprint 2 has a larger technical pressure, which makes scope discipline more important rather than less. Plan the smallest increment that can prove the persistence change without quietly bundling unrelated feature work into it.

### Begin with Sprint 1 evidence

Read the M6 retrospective, current Definition of Done, open review findings, protected tests, and carry-forward question before choosing Sprint 2 scope.

### Record the Sprint 2 decision

The Product Owner creates `docs/decisions/m7-sprint-scope-decision.md`. Keep the same decision shape you already know:

- the observable increment;
- acceptance criteria inside the sprint;
- work explicitly outside the sprint;
- evidence supporting the scope;
- individual ownership;
- the protected behaviors that must still pass after the data-layer change;
- the most important known risk or unresolved question carried from Sprint 1.

**Scope rule:** changing the storage mechanism is enough technical pressure for one sprint. Do not use persistence as an excuse to add unrelated features simply because the module number changed.

### Update the standard before judging the result

The Quality Lead reviews `docs/definition-of-done.md` before Sprint 2 work is evaluated. Keep the existing checks unless there is a recorded reason to change them. Add a persistence-specific check only when the technical requirement is confirmed and another person can reproduce it.

### Plan around the regression suite

The Developer does not begin by deleting tests that fail after the migration. The first question is whether the behavior was supposed to change. Existing tests are evidence of the contract Sprint 2 inherits.

### Ready to build

The pod can name what changes internally, what must remain observable from the outside, who owns each slice, and which evidence will tell you if the change broke something.
