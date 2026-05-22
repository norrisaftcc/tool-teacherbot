# Apply — Your first spike prototype

**Slot:** Apply (hands-on, narrow scope)
**Time:** ~60 minutes
**Goal:** Run one narrowly-scoped experiment that changes one thing about your Week 2 baseline. Write up what happened in one paragraph.

This is the rhythm Manning's textbook uses for the whole term — Meeting A teaches a concept, Meeting B is studio, and a **mid-week "spike prototype"** is the one piece of new work that feeds into the eventual capstone. Get used to this shape. You'll do a spike most weeks.

---

## What a spike is

A spike is **one experiment, narrowly scoped, designed to answer one question.** Not a project. Not a rewrite. One change, measured, written up.

Compare:

- ❌ "I'm going to rebuild my model with more layers and dropout and a different optimizer and see if it gets better."
- ✅ "I'm going to add a second hidden layer and see if validation accuracy goes up or if overfitting gets worse."
- ✅ "I'm going to train for 20 epochs instead of 5 and see when overfitting starts."
- ✅ "I'm going to use `batch_size=32` instead of `128` and see what happens to the loss curve."

Notice the pattern: **one change, one comparison, one answer.**

## Pick one change

Pick **one** of these to try. (If something else interests you, go for it — but only one thing.)

| Option | What to change | What you're testing |
|---|---|---|
| A | Train for 20 epochs instead of 5. | Where does overfitting start? When does the train/val gap appear? |
| B | Add a second `Dense(128, activation="relu")` layer before the output. | Does more capacity help, or does it just overfit faster? |
| C | Change `optimizer="rmsprop"` to `optimizer="adam"`. | Does the optimizer matter on this dataset? |
| D | Change batch size to `32` (smaller) or `512` (larger). | How does batch size affect training speed and final accuracy? |
| E | Change the first layer to `Dense(32, activation="relu")` (smaller). | Is 128 units overkill? |

The point is **not** to pick the "right" one. Pick whichever you're most curious about.

## Run the experiment

1. **Copy your `hello_keras.ipynb` to a new file**: `week-02/spike_<your-change>.ipynb`. Example: `spike_more_epochs.ipynb`, `spike_extra_layer.ipynb`.
2. Make **only the one change** you picked. Nothing else.
3. Re-run the whole notebook from the top.
4. Record the new test accuracy and look at the training curves.

## Write the spike report

In your `week-02/` folder, create a file `spike_report.md`:

```markdown
# Week 2 Spike Report — [your one-line description]

## The change
**Baseline:** [one sentence — describe what hello_keras.ipynb does]
**Change:** [one sentence — what's different in spike_<...>.ipynb]

## Results

| Metric                | Baseline | Spike   |
|-----------------------|----------|---------|
| Final train accuracy  | ____     | ____    |
| Final val accuracy    | ____     | ____    |
| Final test accuracy   | ____     | ____    |
| Train/val gap (final) | ____     | ____    |
| Training time (rough) | ____     | ____    |

## Training curves
[Embed or link to the loss + accuracy plots from the spike notebook.]

## Error analysis (one paragraph, 3–5 sentences)
What does this change tell you about the model? Pick **one** observation that's
not obvious from the numbers above. Did overfitting start earlier or later?
Did the model get *confidently* wrong on different examples than baseline?
Did the training curves look healthier or messier?

## What I'd do next
One sentence. "If I had another day, I'd try ___."
```

## What we're looking for

This is the **first piece of work where stakes start ramping** — not high, but you're being asked to *notice something*. We're grading you on the noticing.

### Earns full credit
- The change really is **only one change** — your spike notebook diffs cleanly against `hello_keras.ipynb`.
- The results table is filled in with real numbers.
- Training curves are present (not just text).
- The error-analysis paragraph says something specific — names a particular failure mode, an observed pattern, or a real surprise.
- "What I'd do next" is a concrete next step, not "study more."

### Loses points
- More than one variable changed (we can't tell what caused what).
- Results table has placeholders.
- Error analysis is "the model got better" / "the model got worse" with no specifics.

## Heads up before [assess.md](assess.md)

The way you submit this week depends on your track. Sacred Flow starts here for Code Builders — open an issue *before* you start the spike, branch off main, do the work on the branch, open a PR with the notebook and report when you're done, and put your retro in the PR description.

Prompt Masters: same artifact (notebook + report), submitted by dragging the `week-02/` folder into your repo.

Full details and rubric in [assess.md](assess.md).

## Where to go next

→ [assess.md](assess.md) — What you submit and how it's graded.
