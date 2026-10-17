CTS-285 · Module 7

## Sprint 2: Change Without Breaking Behavior

Sprint 2 does not restart the process. You bring forward the working system, tests, Definition of Done, review habits, and Sprint 1 findings — then change the system under greater pressure.

Driving question

**Can the system change underneath your feature and still preserve the behavior your evidence says matters?**

### Module learning outcomes

MLO 7.1 → CLO 4 — Protect Behavior During a Data-Layer Change

Use existing acceptance criteria and executable regression tests to identify the behavior that must remain stable while the application's storage mechanism changes.

MLO 7.2 → CLO 4, CLO 5 — Evaluate a Persistence Change Against Evidence

Run and interpret tests and review evidence before and after the data-layer change; distinguish regression defects, migration/data issues, design decisions, and unresolved source questions.

MLO 7.3 → CLO 4, CLO 5 — Deliver Sprint 2 in a Rotated Role

Plan, contribute to, review, and evaluate a second sprint increment in a different assigned role, with reduced scaffolding and individually attributable evidence.

### What changes this sprint

Your role rotates

You hold a different Product Owner, Developer, or Quality Lead responsibility at depth.

Scaffolding fades

Testing, review, Git workflow, and Definition of Done are now established practices rather than new units.

The data layer changes

Persistence replaces the in-memory store with the settled SQLite-backed storage boundary while the existing application interface remains stable.

### What does not change

- there is still no group grade;
- every student still tests, reviews, and contributes;
- GitHub remains the technical source of truth;
- the Definition of Done must still be capable of failing;
- a red test still names a mismatch to investigate, not an automatic code verdict.

### Sprint 2 evidence

You will again leave individually attributable evidence for your contribution, the review you give, and the role you own. The difference is that Sprint 2 expects you to use the workflow with less prompting and to show that previously protected behavior survived a meaningful internal change.

### What comes after Sprint 2

Module 7 is the final product-delivery sprint. Module 8 changes purpose: the pod stops adding features and builds the evidence package the capstone needs to inherit.
