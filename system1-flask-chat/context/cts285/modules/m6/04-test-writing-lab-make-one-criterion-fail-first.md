CTS-285 · Module 6 Lab

## Test-Writing Lab — Make One Criterion Fail First

This lab has two moves: check your reasoning, then prove it in the real application. The first part is a short Canvas New Quiz. The second happens in your GitHub Codespace against the code you carried forward from Module 5.

Outcome

**MLO 6.1 → CLO 4:** write and run an executable test from an acceptance criterion, observe the failing state, investigate what the failure means, revise the right layer, and rerun.

This is controlled practice, not a second code submission.

Your technical evidence stays in GitHub. Do not upload duplicate code to Canvas. You will use this same fail-first habit later when your Sprint 1 Contribution is graded.

### Part 1 — Check the reasoning

Complete the four-item check before you open the code. It focuses on the distinctions that matter once a test turns red: observable criteria, assertions versus implementation, the three suspects, and what fail-first evidence can actually support.

Open M6.2 Quick Check — Before You Run the Test [Canvas link pending]

### Part 2 — Make the behavior fail for real

Return to the application you carried forward from Module 5. Work in your current course Git/GitHub workflow. The point of the lab is the sequence of evidence, not a special lab repository.

Use this criterion unless the behavior already exists in your application.

**Given** a learner has used *n* attempts on a problem with a limit of *L*, **when** the attempts-remaining count is displayed, **then** it reads *L − n*.

1. **Predict the result before touching the implementation.** For the supplied example, after one wrong answer with a limit of two, predict one attempt remaining.
2. **Create or open `tests/test_dataman.py`.** Put the check beside the application rather than inside Canvas.
3. **Write the test before the behavior.** Start with the small plain-Python test below. The tiny runner at the bottom lets this first test execute without adding a testing dependency.

```
import sys

from business_logic import check_answer

BASE = {
    "problem": "6 x 7",
    "expected_answer": 42,
    "try_number": 0,
    "status": "new",
}

def test_attempts_remaining_after_first_wrong_answer():
    result = check_answer(dict(BASE), "41")
    assert result.get("attempts_remaining") == 1

if __name__ == "__main__":
    try:
        test_attempts_remaining_after_first_wrong_answer()
        print("PASS  test_attempts_remaining_after_first_wrong_answer")
        sys.exit(0)
    except AssertionError:
        print("FAIL  test_attempts_remaining_after_first_wrong_answer")
        sys.exit(1)
```

1. **Run it from the project root.** A fresh terminal starts without your environment, so activate it first, then run the suite:
`source .venv/bin/activate`
`PYTHONPATH=. python tests/test_dataman.py`
2. **Read the failure before changing code.** On the Module 5 starter, the expected first result is `FAIL` because `attempts_remaining` does not exist yet. If the suite never starts and reports `ModuleNotFoundError`, fix the path/setup first; that is not a failed test.
3. **Classify what you know.** Ask whether the mismatch points to the code, the test, or the criterion/source. For this supplied criterion, the required behavior is absent and the test checks the predicted observable result, so implementation is the layer to revise.
4. **Preserve the red state in Git history.** Commit the test while it still demonstrates the missing behavior. Your later history should make the before-and-after sequence visible.
5. **Implement the smallest change that satisfies the criterion.** Keep the product rule in the business logic; do not hard-code a replacement number in the template just to make the display look right.
6. **Rerun the test and the earlier tests.** The new test should pass without breaking behavior you already had.

### If your first test passes immediately

Do not damage working code just to manufacture a red result. A test that passes immediately tells you that this behavior may already exist. Choose a different acceptance criterion from your backlog whose required behavior is not yet implemented, predict its result, and repeat the same loop.

**What should I do if the failure is not the one I expected?**

Stop before implementing. Check the test setup and assertion, reread the acceptance criterion, and check the source that supports it. A surprising failure is evidence that your prediction and the system disagree; it is not permission to edit whichever file is closest.

**Code, test, source.** Investigate all three until you can explain the mismatch.

### Part 3 — Protect the behavior against a change you cannot see yet

Every test you have written so far calls `check_answer` directly. That function never reads or writes storage, so none of those tests notice if storage changes. Module 7 replaces the in-memory store with a database. Your suite must be able to tell you whether that swap kept your product rules intact.

Add one more test. It states a product rule you already have: **your progress is remembered between one answer and the next.**

```
from data_store import load_state, save_state


def test_progress_survives_the_round_trip_through_storage():
    save_state(dict(BASE))

    first = check_answer(load_state(), "41")
    save_state(first["state"])

    reloaded = load_state()
    assert reloaded["try_number"] == 1
    assert reloaded["status"] == "retry"
```

This test passes now. That is correct and it is the point — you are recording behavior that works, so that a later change has something to answer to. Notice what it does not say: no database, no table, no file, no connection. It names only the rule. A test written that way survives the change it exists to watch.

Analyst rule

A test that asserts how something is built breaks when you rebuild it. A test that asserts what the product promises tells you whether the rebuild was correct. Write the second kind.

Your runner needs to change too, for two reasons. It runs one named test, and you now have more than one. And storage fails in a way assertions do not: a missing table or a connection that was never opened raises an error before your assertion is ever reached, which ends the run and tells you nothing about the tests after it.

**Replace the whole `if __name__ == "__main__":` block from Part 2 with this one.** It finds every test in the file, so you never edit it again when you add one.

```
if __name__ == "__main__":
    failures = 0
    errors = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS  {name}")
            except AssertionError as exc:
                failures += 1
                print(f"FAIL  {name}: {exc}")
            except Exception as exc:
                errors += 1
                print(f"ERROR {name}: {type(exc).__name__}: {exc}")
    print(f"\n{failures} failing, {errors} errored")
    sys.exit(1 if failures or errors else 0)
```

Run it the same way: `PYTHONPATH=. python tests/test_dataman.py`. You should now see one line per test.

`FAIL` means the test ran and the behavior was wrong. `ERROR` means the test never got far enough to judge. They are different findings and they need different work — and the run still exits nonzero for either, which is what lets a suite gate anything.

### What you should leave with

- a test in `tests/` that expresses an acceptance criterion as observable behavior;
- Git history showing the test before the implementation that made it pass;
- a final green run that includes the earlier behavior you have already protected;
- an explanation of why the first failure implicated the layer you revised;
- one test that reads and writes through `data_store`, so your suite can still tell you something after Module 7 changes where the data lives.

Caution

Keep the test. The lab is formative, but the test suite is not disposable practice. Sprint 1 will add behavior to the same working system, and your tests are what make later change reviewable.
