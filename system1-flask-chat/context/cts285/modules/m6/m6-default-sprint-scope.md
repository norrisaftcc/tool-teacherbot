# Default Sprint Scope — Module 6

**Use this if your pod has not agreed a scope, or cannot.** It is a complete, buildable slice with
acceptance criteria already written. **Building against it is not recorded, does not lower any
rating, and needs no permission.**

Your Product Owner normally decides what the sprint commits to. If that decision has not arrived —
for any reason — you do not wait, and you do not chase anyone. You build this.

Your pod may also use it deliberately: a pod that wants to spend its first sprint learning the
practices rather than arguing about scope is making a defensible call.

---

## The slice

**Show the learner how many attempts remain on the current problem, before the answer is revealed.**

That is the whole sprint. It is deliberately small.

## Where it comes from

This is not invented. It is the requirement your own Module 2 work produced:

> The system must show the learner how many attempts remain on the current problem before it
> reveals the correct answer.

The evidence chain behind it, which you can still read in your own `docs/requirements.md`:

| Evidence | Source |
|---|---|
| A learner was surprised when the device revealed the answer, and could not tell whether they had been wrong or had run out of attempts | The observed practice session |
| Learners make more than one attempt before giving up | The Ms. Alvarez interview |
| *"If after two tries the answer entered is still wrong, DataMan will display the problem with the correct result."* | The manual, printed p. 20 |
| **The manual documents no warning before the reveal** | The manual review |

**That last row is the point of the slice.** The limit is documented; the warning is not. You are not
restoring something the 1977 device did — you are adding something the evidence says a learner
needs, and the manual's silence is why it is a design decision rather than a restoration.

## Acceptance criteria

**AC-1 — The count is visible while the learner can still act.**
**Given** the learner has answered incorrectly at least once and the answer has not been revealed,
**when** the response is displayed,
**then** the number of attempts remaining on this problem is shown.

**AC-2 — The count is true.**
**Given** the learner has used *n* attempts on a problem with a limit of *L*,
**when** the count is displayed,
**then** it reads *L − n*.

**AC-3 — The count is not shown when it would mean nothing.**
**Given** the problem is finished, whether answered correctly or revealed,
**when** the response is displayed,
**then** no attempts-remaining count is shown.

**AC-4 — The limit is stated once.**
**Given** the attempt limit changes,
**when** it is changed in one place,
**then** every display of the count follows it, with no other file edited.

## Why AC-4 is there

It is the rule Module 5 put in front of you in *Run Your First Flask App in Codespaces*, step 4:

> Make the change where that product outcome is decided. Do not hard-code a replacement message into
> the HTML template just because that is where the message appears.

A product rule enforced through more than one entry path is a rule you will eventually break in one
of them. If the limit appears both in your logic and in your template, the two will disagree the
first time anybody changes it, and the display will confidently tell the learner something false.

**AC-4 is the criterion most students fail, and it is the one the reviewer will find.**

## What the limit is

**Read it from your own business logic. Do not type the number into this feature.**

The attempt limit is the Answer Checker's rule and it already exists in your code. This slice
displays it; it does not own it.

**The limit is two**, from the manual, printed p. 20. Your starter already implements it. Read it
from your business logic rather than typing `2` into the display — typing it would pass every test
today and become a lie the moment anybody changed the rule, which is what AC-4 is there to stop.

*You will find course material that says three, and one piece of it may be in your own repository
already.* **Module 3's backlog template carried a story whose acceptance criterion read "Given an
incorrect answer on attempt 3, the system reveals the correct answer."** It was corrected to two on
2026-09-23, so the template you open today says two — but **if you copied that row before then, your
own backlog still says three**, and Module 2 in Canvas still says three until its correction is
re-pasted. The manual says two. The discrepancy is known and is being worked; do not wait on it.

**Build to two, cite the manual page, and record the disagreement in your sprint notes.** Do not
quietly edit your Module 3 backlog to match — a backlog that changed without a record is worse than
one that disagrees with a source, and noticing the disagreement is worth more here than tidying it
away.

*If your implementation and your source disagree about the limit, that is a finding. Record it, say
which you think is right and why, and carry on. A disagreement between code and source is exactly
what Module 6 asks you to be able to spot.*

## Testing it

Every criterion above is checkable without a browser, because the count is computed in your business
logic. **Write the test for AC-2 first and watch it fail** before you build the behavior. A test that
has never failed has proved nothing.

AC-4 is the awkward one to test, and worth the trouble: change the limit in your logic to a different
number, run your tests, and confirm nothing else needed editing.

## Scope controls

Do not add:

- a change to what the attempt limit *is* — this slice displays the rule, it does not set it;
- a warning, a colour, a countdown animation, or any other signal beyond the count;
- persistence — the store is still in memory this module;
- a second game or a Memory Bank;
- anything the evidence table above does not support.

**A sprint that delivers this cleanly, with tests that failed first and a Definition of Done that
something failed, is a complete sprint.** Adding to it does not make it a better one.

## If you are using this because someone is missing

Nothing about that is yours to explain. Say in your sprint record that the pod built against the
default scope, and say nothing about who was absent or why.
`planning/COLD-START-RULE-2026-09-17.md` covers what the course does next, and it is the
instructor's to act on, not yours.
