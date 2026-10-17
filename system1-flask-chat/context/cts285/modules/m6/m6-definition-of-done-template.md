# Definition of Done — Module 6

**Your Quality Lead owns this standard and adapts it for your pod.** This is the course-supplied
starting point.

**Use it unchanged if your pod has not agreed a standard, or cannot.** Using it as supplied is not
recorded, does not lower any rating, and needs no permission. You are graded on applying a standard
honestly to your own work, never on having written a bespoke one.

Copy this file to `docs/definition-of-done.md` in your own repository. Replace every `[bracketed
prompt]` and delete the brackets before you submit.

---

## What a Definition of Done is for

**A standard that cannot fail is not a standard.** It is a description of work you have already
done, written after the fact.

The test is simple: before you check your increment against this list, you should not be able to
predict that everything passes. If you can, the list is too weak to be worth applying.

**Finding a failure is a normal outcome, not a bad one**, and most first sprints find one. But a
clean pass against a real standard is also a normal outcome. What is graded is whether the standard
could have failed and whether you applied it honestly — never the number of failures you report.

---

## The checklist

A slice is done when every line below is true of it. `DoD-01` through `DoD-06` are the supplied
minimum. Your pod may add lines; it may not delete one without recording why.

| ID | The slice is not done until | Who can check it |
|---|---|---|
| DoD-01 | Every acceptance criterion the slice claims has a test that failed before the behavior existed and passes now | Anyone, from the commit history |
| DoD-02 | All tests pass, including the ones written for earlier slices | Anyone, by running them |
| DoD-03 | A product rule appears in exactly one place in the code | A reader who searches for the value |
| DoD-04 | Behavior taken from the 1977 manual cites its page | A reader, against the manual |
| DoD-05 | Another person has run the slice — not read it, run it — and recorded what they saw | The person who ran it |
| DoD-06 | The work is merged to the pod's shared branch, not sitting on a local one | Anyone, from the repository |

**DoD-03 is the one most slices fail**, and it is the one worth keeping. A rule enforced through two
entry paths is a rule you will break in one of them.

**DoD-05 is the one that needs another person**, and it is the one to substitute if nobody is
available. See *If you are working alone* below.

### Lines your pod may want to add

Add a line only if you can say who checks it and how. A line nobody can check is decoration.

- `[DoD-07 — a line your pod adds, with who can check it and how]`
- `[DoD-08 — delete this row if your pod adds only one]`

### Lines your pod removed

| ID | Why it was removed |
|---|---|
| `[DoD-NN]` | `[the reason — "we ran out of time" is not one]` |

**Delete this table if you removed nothing.** Removing nothing is the normal case.

---

## The result

Fill this in against your own slice, at the end of the sprint. **Publish it including the failures.**

| ID | Result | Classification | Reason |
|---|---|---|---|
| DoD-01 | `[met / not met]` | `[fix now / accept and document / out of scope / —]` | `[what you found]` |
| DoD-02 | `[met / not met]` | `[…]` | `[…]` |
| DoD-03 | `[met / not met]` | `[…]` | `[…]` |
| DoD-04 | `[met / not met]` | `[…]` | `[…]` |
| DoD-05 | `[met / not met]` | `[…]` | `[…]` |
| DoD-06 | `[met / not met]` | `[…]` | `[…]` |

### The three classifications

Every line that is not met gets exactly one. **All three are legitimate outcomes.**

- **Fix now** — it is small enough and central enough that the slice is not shippable without it.
- **Accept and document** — the slice ships with a known shortfall, named here so the next sprint
  can see it. This is the honest answer more often than students expect.
- **Out of scope** — the line does not apply to this slice. Say why, not merely that it does not.

**The reason must refer to the work, not to the deadline.** *"We ran out of time"* describes your
week; it says nothing about the software. *"The count is correct but only tested at the default
limit"* is a reason.

### One thing you must not do

**Do not mark a line met that you did not check.** A checklist reporting a pass that did not happen
is worse than no checklist, because the next person trusts it. This is the only failure mode in this
artifact that cannot be classified and accepted — every other outcome above is defensible.

---

## If you are working alone

If your pod is reduced and DoD-05 has nobody to satisfy it, substitute this and say you did:

> Leave the slice for a day, then run it yourself against the acceptance criteria as written, not
> against what you remember building. Record what you saw.

That is weaker than another person and you should say so in the reason column. It is not a penalty
and it is not your failure. `planning/COLD-START-RULE-2026-09-17.md` covers what the course does
next, and it is the instructor's to act on, not yours.

**Nothing about who was absent belongs in this file.**

---

## How this is graded

The Sprint 1 Contribution rubric reads this artifact for one thing: whether you held your own work
against a standard capable of failing, and accounted for what did not meet it.

**A clean result is not worth fewer marks than a failing one.** What is graded is whether the
standard was specific enough to have caught a problem and whether you applied it honestly — both
checkable against your own repository. If every line passes and the standard is real, that is a good
sprint, and it is marked as one.

What scores badly is a standard that *could not* have failed: lines restating what the code already
does, or lines nobody could check. **Do not invent a failure to look honest** — a manufactured
failure is a false record, and it is the same defect as a false pass.

The Quality Lead is additionally graded, through the common Role Record rubric, for owning the standard itself —
whether it is checkable, whether the pod could apply it, and whether it was set before the work
rather than after.
