CTS-285 · Module 1 · 1.4

## M1.4 — The Systems Development Life Cycle (SDLC)

You now know what analysis and design do. The SDLC answers the next question: **where do those activities fit in the larger work of developing and improving a system?**

### The development life cycle

**Planning**
Should we pursue this work, and what constraints shape it?

→

**Analysis**
What problem and requirements must be addressed?

→

**Design**
How should the solution work?

→

**Implementation & evaluation**
Build, test, deliver, review, and improve.

Analyst rule

**The SDLC names categories of work. A methodology organizes how a team moves through and repeats that work.**

### Two ways to organize the same work

#### Plan-driven / sequential

The team completes substantial planning, analysis, and design before most implementation begins. Later work depends heavily on earlier decisions, so late change can be costly.

#### Iterative / incremental

The team works in smaller increments and revisits analysis, design, implementation, testing, and review as the product grows. Evidence from one increment changes what happens next.

### How CTS-285 uses the life cycle

The DataMan project does not restart in every module. It moves through the same development work with increasing independence:

Course work | Life-cycle role

**M1–M2** | Investigate the existing system, evidence, stakeholders, needs, and requirements.

**M3** | Turn validated requirements into product work and project decisions.

**M4** | Investigate implementation questions and create build-ready design evidence.

**M5** | Build the first Flask implementation from the accumulated evidence.

**M6–M7** | Use short sprint cycles to extend, test, review, and revise the working product.

**M8** | Evaluate what is ready to hand forward and what remains unresolved.

### Where Scrum appears

Modules 6 and 7 use the course's practical Scrum-style sprint workflow: a bounded increment, defined roles, explicit acceptance criteria, testing, review, and a decision about what carries forward. You are not studying Scrum as a certification vocabulary unit; you are using an iterative method to manage real product work.

### The life cycle is not a one-way staircase

Even in a plan-driven project, new evidence can force earlier decisions to be revisited. In iterative work, that feedback loop is expected. Testing can expose a weak design. Review can expose a weak requirement. A technical constraint can force the team to reconsider scope.

****A test fails because the requirement itself was ambiguous. Which phase “owns” the problem?****

The failure appeared during implementation/testing, but resolving it requires returning to analysis evidence and clarifying the requirement. The life cycle connects the work rather than isolating it.

****Why use smaller increments?****

Smaller increments make it easier to test assumptions, inspect consequences, obtain feedback, and revise before too much work depends on a weak decision.

Outcome

Explain the major SDLC activities, distinguish the life cycle from a methodology, and describe how CTS-285 moves the DataMan project through plan-driven and iterative/incremental work.

**Next:** M1.5 shifts from defining the discipline to reading a real system like an analyst: identifying behavior, structure, evidence, and uncertainty.

### Content attribution

Concepts are adapted and summarized from Dennis, A., Wixom, B. H., & Roth, R. M. (2012), *Systems Analysis and Design* (5th ed.), with course-specific examples and instructional framing.
