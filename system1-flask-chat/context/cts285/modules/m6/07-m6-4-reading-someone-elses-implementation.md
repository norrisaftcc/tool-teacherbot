CTS-285 · Module 6.4

## Reading Someone Else’s Implementation

Code review is not a hunt for stylistic differences. It is an evidence check: what behavior is claimed, what behavior can you reproduce, and what source settles the disagreement?

Outcome

**MLO 6.2 → CLO 4, CLO 5:** evaluate an implementation against source evidence, acceptance criteria, and observed behavior rather than personal preference.

### Read the claim before the code

Before reviewing a file, identify the acceptance criterion or behavior the change claims to satisfy. Without that reference point, review collapses into “I would have written it differently.”

### Run it, then read it

A review that only reads code can miss behavior that looks correct on the page and fails when executed. Use the comparative pass:

1. **Trace the claim.** Find the story, acceptance criterion, manual page, requirement, or decision the change depends on.
2. **Run the relevant tests.** Confirm the reviewed version actually executes.
3. **Run your protected tests against it when appropriate.** A change may satisfy its new criterion and break earlier behavior.
4. **Compare the result to the evidence.** Separate observable mismatch from design preference.
5. **Write the finding so another developer can act on it.**

Self-check

**Did I run the code, or only read it?** “Looks fine” is often evidence of reading, not evidence of behavior.

### Classify the finding

Classification | Use it when

**Must fix** | The implementation contradicts required behavior, breaks protected behavior, or cannot run.

**Should fix** | The issue weakens maintainability or evidence quality but does not currently violate the acceptance criterion.

**Nitpick** | The suggestion is low-impact and should never be presented as a defect.

**Decision / source question** | The code and test expose an unresolved design choice, missing record, or source ambiguity rather than a settled defect.

### Write a review that can be acted on

A useful finding contains four parts:

1. **Observation:** what you ran or found.
2. **Evidence:** the criterion, test, source, or prior behavior that establishes the expectation.
3. **Classification:** must fix, should fix, nitpick, or decision/source question.
4. **Next move:** the smallest action that would resolve or record the finding.

Example

The count shows `2` after one wrong answer. AC-2 requires *L − n*; with a limit of 2 and one attempt used, the expected value is 1. **Must fix.** Check whether the display is reading the configured limit or repeating the limit unchanged.

### A design difference is not automatically a defect

If two implementations satisfy the same observable behavior in different ways, review the evidence before insisting on one design. Ask whether an earlier decision, architecture constraint, or source requires the difference to be resolved.

### What comes next

The Code Review Lab gives you a supplied target first. You will practice the comparative pass before your review of another implementation becomes graded evidence.
