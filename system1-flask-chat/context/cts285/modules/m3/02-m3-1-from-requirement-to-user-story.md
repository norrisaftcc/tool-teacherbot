CTS-285 • Module 3 • M3.1

## From Requirement to User Story

A requirement tells the team what the system must do or what quality it must have. A user story reframes that requirement as useful product work from the perspective of someone who needs value from the system.

Analyst rule

**The requirement does not disappear.** When you create a user story, you are not replacing the requirement or inventing a new need. You are translating a validated requirement into a unit of product work while preserving traceability to the evidence and requirement that justified it.

### Requirement versus user story

#### Requirement

**Focus:** what the system must do or what quality it must possess.

**Example:** The system shall provide feedback after a learner submits an answer.

**Question it answers:** What capability or quality is required?

#### User Story

**Focus:** who needs the capability, what they need, and why it matters.

**Example:** As a learner, I want feedback after I submit an answer so that I know whether I should continue or try again.

**Question it answers:** Who receives value, what do they need, and why?

### The common story pattern

**As a** [user or role], **I want** [capability or action], **so that** [value or reason].

The pattern helps a team keep three things visible:

- **User/role:** who receives the value;
- **Need:** what capability or outcome is required;
- **Value:** why the capability matters.

Analyst rule

**The template is not the goal.** A sentence can match the “As a / I want / so that” pattern and still be weak product work. A useful story must remain grounded in a real need, describe meaningful value, and be clear enough to discuss and refine.

### Watch what changes—and what does not

**Example 1 — Preserving a learner need**

**Requirement:** The system shall allow a learner to retry an incorrect answer.

**Weak story:** As a developer, I want a retry button so that I can add retry functionality.

**Stronger story:** As a learner, I want another attempt after an incorrect answer so that I can correct my work without immediately being given the answer.

**Why stronger?** It keeps the focus on learner value instead of an implementation detail.

**Example 2 — Avoiding a solution disguised as a story**

**Requirement:** The system shall preserve learner progress between sessions.

**Weak story:** As a learner, I want a MySQL database so that my work is saved.

**Stronger story:** As a learner, I want my progress preserved between sessions so that I can continue without starting over.

**Why stronger?** The requirement establishes the needed outcome. The team can decide later how to implement persistence.

**Example 3 — Not every requirement maps to only one story**

A broad validated requirement may produce more than one story when different users, values, or pieces of work need to be handled separately.

The goal is not a forced one-to-one conversion. The goal is traceable, understandable product work that still represents the validated need.

### A useful story passes four checks

#### Traceable

You can point to the requirement or evidence that justifies the story.

#### User-centered

The story identifies who receives value rather than centering the developer or technology.

#### Value-focused

The “so that” explains why the capability matters instead of repeating the “I want.”

#### Refinable

The story is clear enough for the team to discuss, test, estimate, split, or revise.

### Traceability in your DataMan project

When you begin building your DataMan backlog, each story should point back to the requirement that justifies it. A simple relationship might look like this:

Requirement ID | User Story | Why this story exists

FR-03 | As a learner, I want another attempt after an incorrect answer so that I can correct my work. | The validated requirement establishes retry behavior after an incorrect response.

Caution

**Before you move on.** When you see a requirement, do not immediately fill in the story template. First identify the user, the actual need, and the value. In the next activity, you will practice separating those pieces before writing complete stories.
