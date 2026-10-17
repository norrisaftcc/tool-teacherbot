# DataMan Product Backlog

> Replace all bracketed prompts with your own project work. Delete the prompts before submitting.

This is your primary evaluated Module 3 artifact. It turns your validated DataMan requirements into a traceable, testable, prioritized product backlog that another team member could actually use.

Do not recreate your M2 analysis here. Pull requirement IDs and rationale directly from `docs/requirements.md` — that file is the direct input to this backlog, not a separate exercise.

## Before you start

Have these open:

- `docs/requirements.md` — your validated requirements and their IDs
- `docs/decisions/m3-backlog-triage-record.md` — what backlog triage taught you about readiness, dependencies, effort, and uncertainty
- `docs/decisions/m3-product-owner-decision-record.md` — what the sprint simulation taught you about capacity, tradeoffs, and priority

## The decision chain this backlog must show

**Validated Requirement &rarr; User Story &rarr; Acceptance Criteria &rarr; Effort / Dependency &rarr; Priority &rarr; Rationale**

Every row below must make that chain visible. A story with no requirement ID is not backlog-ready.

## ID scheme

- Use `US-01`, `US-02`, `US-03`, ... for Story ID. Numbers do not need to match requirement numbers.
- Cite the requirement ID each story traces to, using the IDs you already established in M2: `FR-01`, `FR-02`, ... for functional requirements, `NFR-01`, `NFR-02`, ... for non-functional requirements.
- If one requirement produces more than one story, reuse the same requirement ID in the Requirement ID column for each story.
- If a story does not trace to any requirement in `docs/requirements.md`, it does not belong in this backlog yet. Go add or confirm the requirement first, or leave the story out.

## Worked example

This row shows the shape only. It is grounded in the DataMan manual's documented Answer Checker behavior (two tries, then reveal). Do not copy this row's content into your own backlog — write your own stories from your own requirements.

| Story ID | Requirement ID | User Story | Acceptance Criteria | Relative Effort | Dependency / Constraint | Priority | Priority Rationale |
|---|---|---|---|---|---|---|---|
| US-01 | FR-02 | As a student user, I want the Answer Checker to tell me how many attempts I have left, so that I understand why the correct answer is revealed instead of assuming the device is broken. | Given an incorrect answer on attempt 1, the system displays one attempt remaining. Given an incorrect answer on attempt 2, the system reveals the correct answer. | Smaller | None identified | High | Directly supported by manual p. 20 Answer Checker behavior; low effort, and confusing feedback here undermines trust in every other feature. |

## Your backlog

Add one row per story. Include at least [8] stories that together cover your functional and non-functional requirements. Add rows as needed — do not compress unrelated stories into one row to hit a minimum.

| Story ID | Requirement ID | User Story | Acceptance Criteria | Relative Effort | Dependency / Constraint | Priority | Priority Rationale |
|---|---|---|---|---|---|---|---|
| US-01 | [FR-__ or NFR-__] | As a [user], I want [capability], so that [value]. | [Observable, testable condition(s) — what would make another team member agree this story is done] | [Smaller / Medium / Larger] | [Dependency, blocker, constraint, or "None"] | [High / Medium / Low] | [Why this priority is defensible given value, effort, dependency, risk, and stakeholder need] |
| US-02 | [FR-__ or NFR-__] | As a [user], I want [capability], so that [value]. | [Observable, testable condition(s)] | [Smaller / Medium / Larger] | [Dependency, blocker, constraint, or "None"] | [High / Medium / Low] | [Rationale] |
| US-03 | [FR-__ or NFR-__] | As a [user], I want [capability], so that [value]. | [Observable, testable condition(s)] | [Smaller / Medium / Larger] | [Dependency, blocker, constraint, or "None"] | [High / Medium / Low] | [Rationale] |

[Add additional rows until every functional and non-functional requirement in `docs/requirements.md` is represented by at least one story.]

## Relative effort scale

Use only three relative-effort levels: **Smaller, Medium, Larger.** Write out the full word in your Relative Effort column (`Smaller`, `Medium`, or `Larger`), not the single-letter abbreviation `S` / `M` / `L` shown in the DataMan Product Backlog assignment page's format example — that abbreviation exists there only to keep the sample row compact. Use the same full-word form for every row so your backlog reads consistently. Do not assign a numbered points scale or an hour estimate to any story — that level of formal estimation ceremony is out of scope for this course.

- **Smaller** — limited scope, familiar behavior, few dependencies.
- **Medium** — more behavior, more coordination, or some uncertainty.
- **Larger** — broad scope, several dependencies, significant uncertainty, or likely needs to be split before implementation.

## Revision notes

Use this space to record what backlog triage and the Product Owner sprint simulation changed about your thinking. This is not a separate reflection assignment — it is a short trace of your own revision so the reviewer can see your reasoning evolve.

- **What backlog triage changed:** [Name a specific item whose readiness, dependency, or effort call you revised after the triage simulation, and why.]
- **What the sprint simulation changed:** [Name a specific priority you kept or changed after the capacity/complication round, and why.]

## Final quality check

Before submitting, confirm:

- [ ] Every story has a Story ID and traces to a Requirement ID from `docs/requirements.md`.
- [ ] Every story identifies a user and the value the story delivers.
- [ ] Acceptance criteria are observable and testable, not vague.
- [ ] Relative effort uses only the words Smaller / Medium / Larger — no numbered points scale and no hour estimates.
- [ ] Dependencies and constraints are recorded honestly, including "None" where there are none.
- [ ] Every priority has a rationale that names a factor (value, effort, dependency, risk, stakeholder need) — not just "important."
- [ ] Revision notes show what changed after backlog triage and the Product Owner sprint simulation.
- [ ] This file is saved as `docs/product-backlog.md`, committed, and synced to GitHub.
