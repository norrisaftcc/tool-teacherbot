CTS-285 · Module 6.2

## From Acceptance Criterion to Executable Test

In Module 3, you wrote acceptance criteria to describe how you would know a story worked. In Module 5, you checked behavior by running the path and observing the result. Now the check becomes executable: the machine can ask the same question again every time the code changes.

Outcome

**MLO 6.1 → CLO 4:** convert an existing acceptance criterion into an executable test that can demonstrate failure before the required behavior exists and success after the behavior is correctly implemented.

### The criterion is the reference point

A useful test does not begin by asking, *What does my code do?* It begins by asking, *What behavior is supposed to be true?* The acceptance criterion gives you the behavior to predict. The test turns that prediction into a check.

A supplied Sprint 1 criterion

**Given** a learner has used *n* attempts on a problem with a limit of *L*, **when** the attempts-remaining count is displayed, **then** it reads *L − n*.

Before you write code, make the expected behavior concrete. If the limit is 2 and the learner has used 1 attempt, the predicted result is **1 attempt remaining**. That prediction can become an assertion.

### Assertion is not implementation

An **assertion** states what result must be true. An **implementation step** changes the program so the result becomes true. Keeping those separate matters because the test should be able to disagree with the code.

Kind | Example | Job

**Assertion** | `assert result["attempts_remaining"] == 1` | Checks the observable result predicted by the criterion.

**Implementation** | Add logic that calculates and returns the attempts remaining. | Changes the program so the required behavior can exist.

### Write the question before you write the answer

The Module 5 starter gives you a useful testing seam: `check_answer()` is a plain Python function. You can call it directly without starting Flask, opening a browser, or adding a new testing framework.

```
from business_logic import check_answer

BASE = {
    "problem": "6 x 7",
    "expected_answer": 42,
    "try_number": 0,
    "status": "new",
}

def test_attempts_remaining_after_first_wrong_answer():
    result = check_answer(dict(BASE), "41")
    assert result["attempts_remaining"] == 1
```

Against the starter as it currently exists, that test does not pass. The returned result has no `attempts_remaining` value yet. That is useful evidence because this criterion describes behavior that has not been built.

Analyst rule

**A useful red result is a result you understand.** Run the test before the behavior exists, confirm that it fails for the reason you predicted, and preserve that evidence before you implement the change.

### A failure gives you suspects, not a verdict

When a test fails, resist the fastest conclusion. The failure tells you that two things do not agree. Your job is to find out why.

The code

The criterion and test are sound, but the implementation does not produce the required behavior.

The test

The assertion, setup, or predicted result does not actually represent the criterion.

The source or criterion

The statement you tested is vague, incomplete, or in conflict with stronger evidence.

This course found a real example while preparing Module 6. A test written from an inherited course claim disagreed with the working starter. The failure did **not** prove the starter was wrong. Checking the original DataMan manual showed that the inherited claim was wrong and the starter matched the source.

Analyst rule

**When a test fails, there are three suspects: the code, the test, and the source the test was written against. Do not convict the first one you think of.**

### What red → green actually gives you

A fail-first sequence is stronger than a test written only after implementation because it shows that the test was capable of detecting the missing or different behavior. When the same test later passes after the implementation changes, you have a traceable before-and-after result.

It still does not make the source automatically correct. Traceability matters. A green test proves that the implementation agrees with the test. Evidence is what tells you whether the test was asking the right question.

The loop you will use

**acceptance criterion → predicted behavior → executable test → fail → investigate → classify the problem → revise the right layer → rerun**

**Next:** the Test-Writing Lab begins with a short reasoning check, then moves immediately into your real Codespace. You will make one criterion fail for an expected reason before you make it pass.
