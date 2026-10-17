CTS-285 · Module 8.4

## Seed the Risk Register

The capstone does not need a full risk-management unit from CTS-285. It needs a small, credible starting register that names what your own evidence says could threaten the project next.

### Start with risks you already discovered

Use Sprint 2's retrospective, code-review findings, unresolved source questions, design dependencies, and known scope constraints. A useful risk is specific enough that the next course can recognize when it is beginning to happen.

Weak

The code might not work.

Stronger

The persistence change may preserve current tests while losing data between sessions because the existing suite checks behavior inside one run only.

### Seed, do not inflate

Create a small set of risks the receiving team can actually use. Each row should include:

- a concrete risk statement;
- category: technical, schedule, resource/dependency, or scope;
- likelihood: Low / Medium / High;
- impact: Low / Medium / High;
- a trigger or evidence signal;
- a mitigation or next action;
- an owner or receiving-role responsibility;
- status.

### Risk is not the same as an issue

A risk might happen. An issue is already happening. If the product-selection decision or design-consult dependency is unresolved at handoff, record it honestly as an open dependency/issue rather than pretending it is only a future possibility.

### Use evidence from the semester

At least one seeded risk should trace directly to a Sprint 1 or Sprint 2 retrospective/review finding. The register should show that project learning survived the module boundary.

Your artifact

`docs/capstone/risk-register.md`. This is a seeded handoff tool, not a separate graded risk-management project.
