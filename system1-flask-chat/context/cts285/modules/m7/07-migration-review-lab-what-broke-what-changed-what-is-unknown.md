CTS-285 · Module 7 Lab

## Migration Review Lab — What Broke, What Changed, What Is Unknown?

Two broken storage implementations can produce the same failing test. This lab is about diagnosis before repair: use evidence to separate symptom from cause and decide what the finding actually means.

Outcome

**MLO 7.2:** distinguish regression defects, persistence/data failures, design decisions, and unresolved source questions using evidence rather than preference.

### Setup

Activate the same virtual environment used for the working application:

```
source .venv/bin/activate
```

Your instructor will provide two controlled variants of `data_store.py`. Save your own file first. Take each variant in turn. Copy it into your project root and name it `data_store.py`, because that is the name your application and your tests import. Do not merge either variant into your working Sprint 2 implementation. Put your own `data_store.py` back when the lab is done.

### Pass 1 — run before reading the code

For each supplied variant:

1. Run the same M6 regression suite.
2. Record which tests remain green and which test fails.
3. Write a diagnosis based only on the test evidence.
4. State what the evidence does *not* yet tell you.

### Expected observation

Both supplied variants leave the three pure-logic tests green and turn the storage-boundary test red with the same symptom: the wrong answer was not remembered.

### Pass 2 — inspect the implementation

Now inspect the two variants and classify the cause.

Variant | What actually happens | Classification

**Write never lands** | `save_state()` accepts the call but does not preserve the new state | Persistence/data defect at the write boundary

**Load reseeds** | `save_state()` writes, but `load_state()` ignores saved state and returns the seed | Persistence/data defect at the read boundary

### Pass 3 — separate migration findings from unrelated failures

For each finding below, decide whether it is a regression defect, persistence/data defect, design decision, unresolved source question, or unrelated defect:

- the storage test fails after the swap while pure business-logic tests remain green;
- the application returns HTTP 405 before the data layer is reached;
- a legacy test encodes an internal storage detail that the requirement never promised;
- the source material does not establish what should happen after an interrupted attempt;
- the team changes a test only because the new implementation currently fails it.

Analyst rule

**Do not repair the symptom until the evidence tells you which boundary failed.**

### Your review record

For each supplied variant, record:

- observed test evidence;
- cause after inspection;
- classification;
- the smallest justified repair;
- the test you would rerun to verify the repair;
- one thing a green result would still not prove.

**Next:** use the same evidence discipline in Sprint 2 contribution and code review. The graded work is your own; the supplied failures are controlled practice.
