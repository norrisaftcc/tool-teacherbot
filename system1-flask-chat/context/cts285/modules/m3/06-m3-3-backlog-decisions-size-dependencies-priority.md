CTS-285 • Module 3 • M3.3

## Backlog Decisions: Size, Dependencies, and Priority

A product backlog is not just a list of good ideas. Product teams must decide what is ready, what depends on other work, what is relatively larger or smaller, and what should happen first when time and capacity are limited.

Analyst rule

**This is where Product Owner thinking becomes visible.** A Product Owner does not simply ask, “Is this feature useful?” The harder question is: **Given value, risk, effort, dependencies, and limited capacity, what should the team work on now—and what should wait?**

### Four lenses for backlog decisions

#### Value

How much does this work matter to users, stakeholders, or the product goal?

#### Relative Effort

Compared with other backlog items, does this appear smaller, similar, or substantially larger?

#### Dependencies

Does another piece of work need to exist, be clarified, or be completed before this item can succeed?

#### Risk / Uncertainty

What is still unknown, technically uncertain, or likely to create rework if ignored?

### Relative effort is not a promise of hours

Early in a project, teams rarely know exactly how long every item will take. Relative estimation helps compare work without pretending the team has perfect information.

**Smaller:** limited scope, familiar behavior, few dependencies.

**Medium:** more behavior, more coordination, or some uncertainty.

**Larger:** broad scope, several dependencies, significant uncertainty, or likely need to split before implementation.

Caution

**Do not confuse “high value” with “do it first.”** A high-value item may still need to wait because a dependency is missing, the story is too large, the acceptance criteria are incomplete, or another item reduces more risk first. Priority is a decision made from several factors—not a popularity contest.

### Dependencies can change the order

#### Example

**Story A:** As a learner, I want to sign in so that my progress can be associated with my account.

**Story B:** As a learner, I want my progress preserved between sessions so that I can continue without starting over.

If the chosen design requires progress to be tied to an authenticated user, Story B may depend on Story A. That dependency affects sequence even if both stories are valuable.

**Dependency does not always mean “blocked forever.”**

The team may split work, mock a dependency, investigate uncertainty, or choose a temporary approach. The important part is recognizing the dependency instead of pretending it does not exist.

**Large stories may need decomposition.**

A story that is too broad to estimate, test, or complete as one unit may need to be split into smaller pieces that still preserve user value and traceability.

Splitting is not about creating tiny tasks for the sake of it. It is about making work understandable and manageable enough for the team to act on.

### Priority is a defensible decision

A useful priority decision explains why one item should move ahead of another. Depending on the situation, the team may consider:

- user or stakeholder value;
- requirement importance;
- risk reduction;
- dependency order;
- relative effort;
- available capacity;
- uncertainty that should be resolved early;
- whether the item is actually ready for team consideration.

Backlog Item | Value | Relative Effort | Dependency | Decision

Learner sign-in | Medium | Medium | Needed before account-based progress | Move earlier if persistence depends on it

Decorative theme selector | Low | Small | None | Defer despite small size

Preserve learner progress | High | Large | May depend on identity/session design | Refine dependency before commitment

### Capacity forces tradeoffs

If the team can handle only a limited amount of work, choosing one backlog item means delaying another. That is not automatically a failure. It is the normal consequence of constrained product development.

Analyst rule

**A stronger Product Owner explanation sounds like this.** “We are prioritizing Story A ahead of Story B because A removes a dependency that blocks two higher-value items. Story B still matters, but committing to it first would increase the risk of rework.”

### Before you move on

For each backlog item, be ready to answer:

1. What value does this item create?
2. How large does it appear relative to other work?
3. What does it depend on?
4. What uncertainty or risk affects it?
5. Given limited capacity, why should it move now—or wait?

**Next:** In the Backlog Triage Lab, you will practice making these decisions with a controlled set of backlog items before the Product Owner Sprint Simulation raises the stakes.
