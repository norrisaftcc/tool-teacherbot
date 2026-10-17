CTS-285 · Module 7 Lab

## Persistence/Regression Lab — Prove What Must Survive

You already know how to write and read executable tests. This lab asks a different question: when storage changes underneath the application, what evidence proves that the product behavior survived?

Outcome

**MLO 7.1 and MLO 7.2:** protect existing behavior during a data-layer change and interpret the evidence before deciding what to change.

### Before you change storage

1. Open the same CTS-285 repository you carried through Sprint 1.
2. From the project root, create and activate the virtual environment if it does not already exist:

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

In a fresh terminal, reactivate it with `source .venv/bin/activate`.

1. Run the Module 6 regression suite **before** replacing the in-memory store.
2. Record which behavior the suite protects and what you predict must remain unchanged after the swap.

Analyst rule

**Run the evidence before the change so you know what “still works” actually means.**

### Build the persistent boundary

Keep `app.py` and `business_logic.py` unchanged. Keep the names and signatures of `load_state()` and `save_state(new_state)`. Rewrite only the body of `data_store.py` so that SQLite sits behind the same interface.

Your artifact

`docs/schema.md` — record the exact one-table schema below and explain briefly why one typed row is enough for the current DataMan state.

```
CREATE TABLE IF NOT EXISTS dataman_state (
    id              INTEGER PRIMARY KEY CHECK (id = 1),
    problem         TEXT    NOT NULL,
    expected_answer INTEGER NOT NULL,
    try_number      INTEGER NOT NULL DEFAULT 0,
    status          TEXT    NOT NULL DEFAULT 'new'
);
```

Save this statement, exactly as printed, as `schema.sql` in the same folder as `data_store.py`. No one supplies this file; you write it. On the first storage call, `data_store.py` reads `schema.sql`, checks for the store, and creates it when needed. The database starts fresh; this sprint does not migrate transient in-memory state.

### Prove two different things

1. Run the unchanged M6 regression suite again. The previously protected behavior should remain green.
2. Run the Flask application:

```
python -m flask --app app run --debug --host=0.0.0.0
```

1. Submit one wrong answer.
2. Stop the application process.
3. Restart it.
4. Submit the second wrong answer.
5. Verify that the reveal occurs because the first wrong attempt survived the restart.

Caution

A green old suite proves protected behavior survived the swap. Only the restart test proves persistence itself.

### Inspect a controlled failure before editing

Your instructor will provide one of the two supplied broken variants of `data_store.py`. Save your own file first. Copy the variant into your project root and name it `data_store.py`. Your application and your tests import a module called `data_store`, so the variant only runs under that name. Run the same suite. In both cases the three pure-logic tests remain green and the storage test turns red. Do not repair immediately. Put your own `data_store.py` back when you have recorded the evidence.

First classify the evidence:

- What passed?
- What failed?
- What does that isolate?
- What would you inspect next?
- What evidence would distinguish a write problem from a load problem?

**Next:** Sprint 2 planning uses this evidence to bound the increment before the migration becomes graded delivery work.
