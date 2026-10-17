CTS-285 · Module 7.3

## Reading Regression Evidence

A failed test after a storage change does not automatically mean the new SQLite code is wrong. Your job is to identify what the evidence actually establishes before you edit anything.

Outcome

**MLO 7.2:** evaluate a persistence change against evidence and distinguish regression defects, migration/data issues, design decisions, and unresolved source questions.

### Classify before you repair

Finding | What the evidence suggests | Do not assume

**Regression defect** | Behavior protected before the storage change no longer holds | That every failure is caused by SQLite

**Data / persistence defect** | State is written, loaded, initialized, or committed incorrectly | That the business rule itself is wrong

**Design decision** | The system boundary legitimately changed and the team must decide how evidence should adapt | That changing a test is always weakening it

**Unresolved source question** | The available requirement or source does not establish the expected behavior | That implementation preference can fill the gap

### Two failures can look similar and mean different things

A write that never commits can appear successful until the process restarts. A load path that reinitializes state on every read can make saved progress disappear. Both are persistence failures, but they point to different evidence and different repairs.

Caution

A routing error that never reaches the data layer may happen during the same sprint, but it is not evidence that the persistence migration failed.

### A green old suite is necessary, not sufficient

The unchanged M6 tests protect behavior across the storage swap. If they fail, you have evidence that something protected changed. If they pass, you know those behaviors survived. You still need the restart-survival test because an in-memory implementation can pass ordinary round-trip checks and still forget everything when the process stops.

Analyst rule

**Green evidence tells you what the test proved. It does not prove everything you hoped the change accomplished.**

### When a test may legitimately change

Revise a test only when the system boundary changed in a way the old test encoded incorrectly and the requirement still supports the new expectation. Record why the test changed. Do not rewrite a test merely to make a failing implementation turn green.

**Next:** the Migration Review Lab gives you a supplied target with mixed findings. Classify each finding before deciding what, if anything, should be changed.
