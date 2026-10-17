CTS-285 · Module 7 · Graded Evidence

## Code Review Given — Sprint 2

Use the review method from Sprint 1 with less prompting. This time, pay particular attention to behavior that worked before the data-layer change and now behaves differently.

### Review file

Create `docs/reviews/m7-code-review-given-<github-username>.md`. Include the same evidence structure you already know: observation, evidence, classification, and next move.

### Sprint 2 review pressure

When a change affects persistence, do not call every difference a regression. Ask which layer the evidence implicates:

- existing product behavior changed unexpectedly;
- data did not migrate or persist as required;
- a design choice changed intentionally and needs a record;
- the source or requirement does not settle the question;
- an old test encodes an assumption that is no longer part of the intended contract.

**Submit in Canvas:** one GitHub link to your review evidence. The grade reads your review, never the quality of the implementation you were assigned.

**Points:** use the same 6-point common review architecture as Sprint 1 unless course-wide reconciliation changes it.
