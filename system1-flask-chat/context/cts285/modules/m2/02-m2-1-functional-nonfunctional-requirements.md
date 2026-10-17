CTS-285 • Module 2.1

## Functional and Non-Functional Requirements

Requirements work is a transferable systems-analysis skill. You will first learn how to distinguish requirement types in ordinary software situations, then apply the same reasoning to the DataMan modernization project.

Outcome

**MLO 2.1** — Classify and evaluate functional and non-functional requirements using system and stakeholder evidence.

### Two Different Questions

### Functional Requirement

**What must the system do?**

A functional requirement describes a behavior, service, calculation, interaction, or capability the system must provide.

### Non-Functional Requirement

**How well—or under what conditions—must it work?**

A non-functional requirement describes a quality or constraint such as performance, security, reliability, usability, accessibility, compatibility, or availability.

Analyst rule

A stakeholder statement is not automatically a finished requirement. Analysts still have to clarify vague language, separate needs from proposed solutions, and decide whether the statement can eventually be verified.

### Controlled Practice: Classify the Skill Before the Case

Do not memorize DataMan examples. Practice the reasoning across different systems so you can transfer the skill to unfamiliar projects.

Statement | Classification | Why

Users can request a password-reset link. | **Functional** | It describes a capability the system provides.

Search results appear within two seconds under normal operating load. | **Non-functional** | It sets a measurable performance condition.

Make the dashboard intuitive. | **Not ready** | “Intuitive” is too vague to test without clarification.

Use MongoDB for customer records. | **Proposed solution** | It specifies an implementation choice rather than the underlying need unless the technology itself is constrained.

### Same Feature, Different Requirement Types

Functional and non-functional requirements often describe different aspects of the same feature.

**Functional:** The system must allow a learner to submit an answer to a math problem and receive correctness feedback.

**Non-functional:** Feedback must be available through keyboard navigation and must not rely on color alone.

### Common Non-Functional Areas

**Performance**
Response time, speed, capacity

**Security**
Authentication, authorization, protection

**Reliability**
Availability, recovery, error tolerance

**Usability**
Learnability, clarity, task completion

**Accessibility**
Perceivable and operable interaction

**Compatibility**
Browsers, devices, environments

### Now Apply the Skill to DataMan

The original DataMan manual is project evidence. It tells you what the 1977 product did and what its designers intended—but it does not automatically tell you what the 2026 web application should do.

Manual Evidence | Analysis | Likely Direction

Answer Checker accepts a problem and answer, gives feedback, and supplies the correct answer after repeated incorrect attempts. | This reveals core learner interaction and feedback behavior. | **Functional requirement candidate**

Memory Bank stores practice problems, tracks correct responses, and displays a score. | This suggests persistence, practice, and progress-feedback capabilities. | **Functional requirement candidates**

The original unit shuts itself off after inactivity to preserve battery power. | The underlying concern matters more than copying the 1977 implementation into a web app. | **Needs further analysis**

The product was intended to provide enjoyable, self-paced mathematics practice for children. | This points toward usability, accessibility, age-appropriate interaction, and feedback qualities. | **Non-functional concerns**

### Not Every Statement Is Ready

“Make DataMan modern.”

That statement may represent legitimate needs, but it is not yet clear or testable. An analyst should ask:

- Modern for whom?
- Which current problem needs to change?
- Does “modern” mean appearance, access, speed, device compatibility, feedback, security, or something else?
- What observable result would show that the change worked?

### Do Not Turn a Solution Into a Requirement

If the evidence says, “Learners lose progress,” do not immediately write:

**Weak:** DataMan must use PostgreSQL.

That is a technical solution. First identify the behavior or quality the system must provide. Design and implementation decisions come later.

### Required Reading

**Handbook of Software Engineering Methods — Requirements**

Read the sections addressing types of requirements, functional requirements, non-functional requirements, and qualities of useful requirements.

**Reading lens:** Does this statement describe what the system does, a quality or constraint on how it operates, or something that still needs clarification?

[Open Required Reading](https://open.oregonstate.education/setextbook/chapter/requirements/)

### Quick Self-Check

****“The system allows a learner to start Number Guesser and enter guesses from 1–100.”****

**Functional.** It describes behavior the system provides.

****“The web application can be operated using keyboard-only navigation.”****

**Non-functional.** It describes an accessibility condition.

****“Make Number Guesser more fun.”****

**Not ready.** It needs elicitation before it can become useful project work.

### What Carries Forward

- Classify requirements by what they communicate—not by the topic or product.
- Use evidence before turning a statement into project work.
- Clarify vague language before treating it as a requirement.
- Keep implementation choices separate until design decisions are justified.
- These requirements will later become user stories, acceptance criteria, and backlog work in Scrum.

Next

### Classify the DataMan Requirements

Apply the transferable classification skill to the project case before moving into requirements elicitation.
