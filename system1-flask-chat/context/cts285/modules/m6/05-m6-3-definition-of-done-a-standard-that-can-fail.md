CTS-285 · Module 6.3

## Definition of Done: A Standard That Can Fail

A working feature is not automatically a finished increment. Sprint work also has to survive the checks your pod agreed would count as done.

Outcome

**MLO 6.3 → CLO 4, CLO 5:** plan and evaluate a sprint increment against an explicit standard that can genuinely pass or fail.

### Done is a standard, not a feeling

A Definition of Done is useful only when it is written **before** the team knows how the increment will turn out. If every line merely restates work you already completed, the checklist cannot expose anything.

Working rule

**A standard that cannot fail is not a standard.** Finding a failure is a normal sprint result. Reporting a pass you never checked is not.

### The course gives you the starting standard

The Quality Lead owns the standard for the pod, but does not have to invent one. The supplied template gives every pod six minimum checks:

ID | The slice is not done until

**DoD-01** | Every claimed acceptance criterion has a test that failed before the behavior existed and passes now.

**DoD-02** | All tests pass, including tests protecting earlier behavior.

**DoD-03** | A product rule appears in exactly one place in the code.

**DoD-04** | Behavior taken from the 1977 manual cites its page.

**DoD-05** | Another person has run the slice and recorded what they observed.

**DoD-06** | The work is merged to the pod's shared branch.

Your pod may add checks. It may remove a supplied check only when the reason is recorded. Using the supplied template unchanged is completely acceptable.

### Not met does not always mean fix now

When a line fails, classify the result instead of pretending the failure did not happen.

Fix now

The shortfall is central enough that the slice should not ship without the repair.

Accept and document

The slice can move forward with a known shortfall that Sprint 2 can see.

Out of scope

The line does not apply to this slice. The reason must explain why.

### The check must be reproducible

Each line should answer two questions: **who can check it?** and **how?** “Looks good” is not a check. “Run the full test suite and confirm all tests pass” is.

**Quick check: which line is stronger?**

**A:** The feature works correctly.

**B:** Every acceptance criterion claimed by the slice has a test, and the complete test suite passes.

**B** is stronger because another person can reproduce the check and determine whether it passed.

Your artifact

The Quality Lead places the supplied template at `docs/definition-of-done.md` before the sprint work is evaluated. Sprint planning comes next, so the pod commits to scope knowing the standard the increment must survive.
