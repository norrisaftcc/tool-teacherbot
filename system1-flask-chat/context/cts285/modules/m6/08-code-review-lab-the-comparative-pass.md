CTS-285 · Module 6 Lab

## Code Review Lab — The Comparative Pass

Before you review a classmate’s implementation for a grade, everyone reviews the same supplied target. Your job is not to find the most problems. Your job is to decide what the evidence actually supports.

Outcome

**MLO 6.2 → CLO 4, CLO 5:** run, compare, classify, and explain findings against acceptance criteria and source evidence.

### The target

This implementation attempts the same attempts-remaining slice used in Sprint 1. It runs. It is not completely correct.

**Acceptance criteria to keep beside you:**

- **AC-1:** after at least one incorrect answer and before reveal, the number of attempts remaining is shown;
- **AC-2:** after *n* attempts with limit *L*, the count reads *L − n*;
- **AC-3:** once the problem is finished, no attempts-remaining count is shown;
- **AC-4:** changing the limit in one place changes every display of the count.

### Business logic

```
ATTEMPT_LIMIT = 2


def attempts_remaining(state):
    return ATTEMPT_LIMIT - state["try_number"]


def check_answer(state, submitted):
    expected = str(state["expected_answer"])
    next_state = dict(state)

    if submitted == expected:
        next_state["status"] = "correct"
        return {
            "message": "Correct.",
            "allow_retry": False,
            "reveal_answer": False,
            "attempts_remaining": attempts_remaining(state),
            "state": next_state,
        }

    next_try = state["try_number"] + 1
    next_state["try_number"] = next_try

    if next_try >= ATTEMPT_LIMIT:
        next_state["status"] = "revealed"
        return {
            "message": f"The correct answer is {expected}.",
            "allow_retry": False,
            "reveal_answer": True,
            "attempts_remaining": 0,
            "state": next_state,
        }

    next_state["status"] = "retry"
    return {
        "message": "Try again.",
        "allow_retry": True,
        "reveal_answer": False,
        "attempts_remaining": attempts_remaining(state),
        "state": next_state,
    }
```

### Display template

```
{% if outcome %}
  <p>{{ outcome.message }}</p>
  {% if outcome.allow_retry %}
    <p>You have {{ outcome.attempts_remaining }} of 2 tries left.</p>
  {% endif %}
{% endif %}
```

### Run before you judge

Put the supplied `business_logic.py` in a temporary folder in your Codespace, or use the instructor-provided copy. Activate your environment in your project root first, with `source .venv/bin/activate`. It stays active when you move to another folder. Then, from the folder holding the supplied file, run:

```
python -c "from business_logic import check_answer; print(check_answer({'problem':'6 x 7','expected_answer':42,'try_number':0,'status':'new'}, '41'))"
```

Record the actual value returned for `attempts_remaining`. Then change `ATTEMPT_LIMIT` temporarily and ask whether the display template would still tell the truth.

### Sort each finding before proposing a fix

Defect

The source or criterion settles the expected behavior and the implementation disagrees.

Decision

The source is silent and one reasonable design differs from another.

Gap

No source or prior decision reaches the question yet.

### Your practice record

For at least three observations, write four short lines in your notes:

1. **What I observed:** include the actual value or behavior.
2. **What evidence applies:** criterion, manual page, requirement, or existing decision.
3. **Classification:** defect, decision, or gap.
4. **Next move:** fix, record the decision, or escalate the unresolved question.

**Do not submit this practice record.** The graded Code Review Given uses the same reasoning structure, but it reads your own review file in GitHub.

**Debrief question**

Which difference was hardest to classify, and what evidence would you need before you could call it a defect?

**Next:** Sprint 1 graded evidence. Your grade will attach to your own contribution, the review you give, and the role responsibility you own — never to whether a teammate’s code is good.
