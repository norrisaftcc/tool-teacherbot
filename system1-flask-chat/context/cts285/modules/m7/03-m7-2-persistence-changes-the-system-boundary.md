CTS-285 · Module 7.2

## Persistence Changes the System Boundary

Sprint 2 changes one internal part of a working system: state that disappeared when the process stopped must now survive. The product behavior is not being redesigned. The storage boundary is.

Outcome

**MLO 7.1:** protect behavior during a data-layer change by identifying what must remain stable while storage changes underneath it.

### What changes and what must not

Changes internally | Must remain stable

The body of `load_state()` and `save_state(new_state)` | Their names, signatures, module path, and the behavior protected by the M6 suite

State moves from memory to SQLite | `app.py` and `business_logic.py` keep using the same storage interface

A schema defines typed persistent fields | The product rules do not change merely because storage changed

### The course schema is deliberately small

DataMan uses one typed table with one current-state row. It mirrors the state the application already keeps in memory. There are no joins and no foreign keys in this sprint.

Analyst rule

**Use enough structure to model the problem correctly, but do not add complexity that the problem does not require.**

A key/value table would be easier to write, but it would hide type decisions by treating every value the same. A small typed table makes the storage choices visible enough to inspect. That does not make this a full data-modeling unit. The entity question here is intentionally simple.

### Reset is part of the boundary change

Sprint 2 does not migrate the old in-memory state into SQLite. The persistent store starts fresh. The question is whether the new store preserves behavior correctly from that point forward, not whether old transient data can be recovered.

### Initialization stays inside the storage boundary

On the first storage call, `data_store.py` checks whether the persistent store exists and creates it from the schema file when needed. Students write that file themselves in the Persistence/Regression Lab: they save the DDL printed there as `schema.sql`, in the same folder as `data_store.py`. There is no separate initialization program for students to run. This keeps setup attached to the component whose responsibility is storage.

Your artifact

`docs/schema.md` — record the one-table schema, the field types, and a short rationale for why that structure is enough for this system state.

### What proves persistence

A green legacy test suite proves that protected behavior still works through the storage interface. It does not, by itself, prove persistence. The new evidence is stronger:

**Persistence criterion:** submit a wrong answer, stop the application process, restart it, submit a second wrong answer, and observe the reveal that depends on the earlier attempt still being remembered.

**Next:** use the controlled persistence/regression lab to compare the protected behavior before and after the storage change using the settled CTS-285 virtual-environment and Flask command sequence.
