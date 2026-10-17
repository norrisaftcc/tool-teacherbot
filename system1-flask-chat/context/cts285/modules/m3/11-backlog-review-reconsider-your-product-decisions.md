CTS-285 • Module 3 • Gauge / Revision

## Backlog Review — Reconsider Your Product Decisions

You have made product decisions in two different constrained situations. Now use what those decisions exposed to improve your own DataMan product backlog before it is evaluated.

Caution

**This is revision, not another assignment.** Do not create a second backlog or start over. Open the DataMan backlog you have been building and make evidence-based revisions to that same artifact.

### Bring three pieces of evidence together

#### 1. Your requirements

`docs/requirements.md`
Use requirement IDs and rationale so every story still traces back to validated need.

#### 2. Your triage decisions

`docs/decisions/m3-backlog-triage-record.md`
Look for lessons about readiness, dependencies, effort, and uncertainty.

#### 3. Your sprint decisions

`docs/decisions/m3-product-owner-decision-record.md`
Look for lessons about capacity, tradeoffs, changing constraints, and priority.

### Make sure your backlog has the required fields

Before you review and revise `docs/product-backlog.md`, confirm that each backlog item includes:

- **Story ID**
- **Requirement ID**
- **User Story**
- **Acceptance Criteria**
- **Relative Effort**
- **Dependency / Constraint**
- **Priority**
- **Priority Rationale**

**If a field is missing, add it before using the review lenses below.** The DataMan Product Backlog assignment that follows this page contains the full final-submission instructions.

### Review every backlog item through six lenses

Lens | Ask yourself | Possible revision

**Traceability** | Can I point to the requirement that justifies this story? | Add or correct the Requirement ID.

**User / value** | Does the story identify who benefits and why it matters? | Repair a solution-focused or circular story.

**Acceptance criteria** | Could another person determine whether this story passed or failed? | Make criteria observable, specific, and testable.

**Scope / effort** | Is the story small enough to discuss, estimate, test, and revise? | Split work that is too broad or clarify relative effort.

**Dependency / uncertainty** | What must happen first? What is still unknown? | Record a dependency, constraint, or unresolved issue.

**Priority** | Given value, effort, dependencies, risk, and limited capacity, does this item belong where I placed it? | Move the item, defer it, or strengthen the rationale.

Analyst rule

**Do not revise just to show activity.** A professional review can confirm that an existing decision still holds. If an item is already traceable, testable, appropriately scoped, and defensibly prioritized, leave it alone. Revision should respond to evidence—not create change for its own sake.

### Make the revision visible in GitHub

1. Open your existing `docs/product-backlog.md` file.
2. Review every item using the six lenses above.
3. Revise only what needs revision.
4. Make sure the backlog still shows traceability to your M2 requirements.
5. Commit the revised file to your CTS-285 repository.

Analyst rule

**Use a meaningful commit message.** Your commit message should communicate the work you actually completed.

**Example:** `Refine DataMan backlog after product review`

**What if I discover a story should be split?**

Split it when the original story is too broad to estimate, test, or move through the product process as one understandable unit. Preserve the same Requirement ID where both new stories still trace to the same validated requirement.

**What if an important story has an unresolved dependency?**

Keep the value visible, but document the dependency and make a defensible priority decision. High value and immediate readiness are not the same thing.

**What if my original priority still makes sense?**

Keep it. Your goal is a defensible backlog, not a required number of changes.

### Ready for evaluation?

Before you move to the DataMan Product Backlog submission, confirm that your file now communicates:

- what the product team should build;
- which requirement each story comes from;
- what must be true for each story to be accepted;
- how relative effort, dependencies, and uncertainty affect the work;
- what is most important and why.
