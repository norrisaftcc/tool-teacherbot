CTS-285 • Module 2.2

## Requirements Elicitation: Find the Need Behind the Request

Real stakeholders rarely hand an analyst a clean, testable requirement. They describe frustrations, wishes, workarounds, assumptions, and solutions. Your job is to uncover the need before the team commits to the wrong work.

Outcome

**MLO 2.2** — Apply elicitation techniques to clarify ambiguous stakeholder statements and identify the need behind a request.

### Elicitation Is More Than Asking, “What Do You Want?”

Stakeholders know their work, but they may not know how to describe a system requirement. They may also jump directly to a preferred solution. Analysts use elicitation to uncover the problem, context, constraints, and success conditions underneath the request.

**Clarify**
What does the stakeholder mean?

**Probe**
What problem is occurring now?

**Observe**
What actually happens in the workflow?

**Confirm**
How will we know the need is satisfied?

### A Professional Elicitation Pattern

1. **Hear the request.** Record what was said without immediately rewriting it as a requirement.
2. **Identify the uncertainty.** Mark vague terms, assumptions, missing actors, missing conditions, and proposed solutions.
3. **Ask a neutral question.** Seek evidence rather than leading the stakeholder toward your preferred answer.
4. **Look for the underlying need.** What problem, outcome, or constraint is actually driving the request?
5. **Confirm success.** Ask what observable result would tell the stakeholder that the problem has been addressed.

Analyst rule

Preserve the stakeholder's words separately from your interpretation. In real projects, that distinction protects traceability and reduces the risk of quietly turning an assumption into a requirement.

### Controlled Practice: What Would You Ask Next?

Before working with the DataMan case, practice the skill in unrelated systems. The goal is transfer: you should be able to recognize ambiguity regardless of the product.

****Stakeholder:** “The advising dashboard needs to be faster.”**

**Weak response:** “So you want us to rewrite it in a faster framework?”

**Stronger questions:**

- Which actions currently feel too slow?
- About how long do they take now?
- At what point does the delay interfere with the advising task?
- What response time would be acceptable for that task?

**Why:** “Faster” may reveal a performance requirement, but only after the analyst identifies the task, current condition, and measurable expectation.

****Stakeholder:** “Put a button on the homepage so employees stop losing the form.”**

**What is suspicious?** The stakeholder has already proposed a design solution.

**Stronger questions:**

- How do employees currently locate the form?
- Where in that process do they get lost?
- How often is the form used?
- What would successful access look like?

**Possible underlying need:** Employees need a reliable, easy-to-find path to the form. A homepage button may be one solution, but it is not yet the requirement.

****Stakeholder:** “Customers keep entering the wrong thing.”**

**What is missing?** We do not know which field, which error, why it occurs, or what the system currently does after the error.

**Useful evidence to seek:** observations, error logs, examples of incorrect entries, user steps, and current feedback.

**Professional lesson:** Sometimes an interview is not enough. Elicitation can include observation, document review, prototypes, and existing system evidence.

### Common Elicitation Mistakes

Mistake | Why It Fails | Better Move

Accepting vague words | Terms such as modern, easy, fast, secure, and intuitive are not testable by themselves. | Ask what behavior or measurable outcome the word represents.

Leading the stakeholder | The analyst may create agreement instead of discovering evidence. | Use neutral questions: “What happens now?” rather than “Wouldn't it be better if...?”

Treating a solution as the need | The team may implement the requested mechanism without solving the problem. | Ask what problem the proposed solution is intended to solve.

Interviewing only one perspective | Different users may experience the same system differently. | Compare stakeholder statements with observation and system evidence.

### Now Apply the Skill to DataMan

The original DataMan manual gives you one kind of evidence: what the 1977 product did and how its designers described the experience. Your next case adds stakeholder evidence about the modernization effort.

As you work through the case, separate what you encounter into four buckets:

**Evidence**
What you can actually support

**Need**
The underlying problem or outcome

**Assumption**
Something not yet verified

**Proposed Solution**
A possible implementation, not automatically a requirement

### Key Takeaways

- Elicitation uncovers needs; it does not simply record feature requests.
- Neutral questions produce better evidence than leading questions.
- Interviews, observation, documents, and system behavior can all provide evidence.
- Vague language must be clarified before it becomes a usable requirement.
- Keep needs separate from proposed solutions until the evidence supports a design decision.

Next

### M2 Simulation — Stakeholder Elicitation Under Pressure

Elicit under a real constraint. You cannot ask everything, so decide which questions earn the evidence you need. Do not try to guess the “correct solution.”
