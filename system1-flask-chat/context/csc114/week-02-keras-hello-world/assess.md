# Assess — What you submit (by track)

**Slot:** Assess (graded; stakes are starting to rise but still forgiving)
**Due:** End of Week 2, before Monday of Week 3.

---

## What you submit (both tracks)

The artifact is the same regardless of track. Files in your `week-02/` folder:

1. **`hello_keras.ipynb`** — the Practice notebook, run end-to-end. Cells executed, outputs visible.
2. **`spike_<your-change>.ipynb`** — your spike experiment notebook. Cells executed, outputs visible. Exactly one variable different from `hello_keras.ipynb`.
3. **`spike_report.md`** — filled in per the template in [apply.md](apply.md). Results table real, training curves embedded or linked, error-analysis paragraph specific.

That's the **artifact**. Both tracks get graded identically on it.

## How you submit — the two tracks split here

### Code Builders track — full Sacred Flow

Sacred Flow this week: **Issue → Branch → Work → Commit → PR → Merge.** No skipping.

1. **Open a GitHub Issue** in your course repo titled `Week 2 spike: <your one-line description>`. Body: which option (A–E from [apply.md](apply.md)) you picked, and your one-sentence hypothesis. *Open this before you start the spike, not after you finish it.*
2. **Branch** off `main`: `week2-yourname` (e.g., `week2-jdoe`).
3. **Commit** as you go. Meaningful commit messages — `add hello_keras notebook`, `spike: switch optimizer to adam`, `spike: add results to report`. Not `wip` or `stuff`.
4. **Open a PR** from your branch to `main` when you're done.
5. **Retro** lives in the **PR description**. 3–5 sentences. Template:

   ```
   ## Retro

   **What worked:** [one specific thing]
   **What surprised me:** [one specific thing — not "everything was new"]
   **What I'd do differently next time:** [one concrete change to my workflow or to the experiment]
   ```

6. **Request review** from your instructor or your assigned peer reviewer. Address any comments. Merge once approved.

If you don't have a peer reviewer assigned yet, your instructor reviews. Tagging them in the PR works.

### Prompt Masters track — drop submission

1. Make sure your `week-02/` folder in your local clone of your course repo has all three files.
2. Push them to your repo via **GitHub Desktop** (`commit to main → push origin`) or via **the GitHub web UI** ("add file → upload files").
3. Done.

No issue, no branch, no PR, no retro required. The artifact is what gets graded.

If you'd like to *try* Sacred Flow this week without committing to the track, go for it — you don't lose anything for trying. We won't enforce it.

## Grading

| Component | Weight | Both tracks |
|---|---|---|
| Practice notebook runs cleanly and outputs are visible | 25% | ✓ |
| Spike notebook is exactly one variable changed | 15% | ✓ |
| `spike_report.md` results table filled with real numbers | 15% | ✓ |
| `spike_report.md` error-analysis paragraph is specific | 25% | ✓ |
| `spike_report.md` "what I'd do next" is concrete | 10% | ✓ |
| Notebooks have reflection / explanation cells, not just code | 10% | ✓ |

**Code Builders also earn process credit:** if your Sacred Flow is complete (issue exists, branch is named clearly, PR has a retro, merged after review), you earn extra credit equivalent to one rubric line. This is on top of the artifact grade, not instead of it.

## What loses points (both tracks)

- Notebook cells weren't actually run before submission (no outputs visible).
- Spike notebook has more than one variable changed from baseline.
- Error analysis is generic ("the model worked well," "training was good").
- Results table has `___` placeholders or "TBD."
- (Code Builders only) Sacred Flow is half-done — issue but no PR, or PR with no retro, or merging your own PR without requesting review.

## Stretch (optional, no extra points)

If you want to push, re-run your spike with **two different random seeds** (set `keras.utils.set_random_seed(42)` and `(43)`) and report whether the difference you saw is real or within run-to-run noise. This is a Week 3 / Manning Ch 2 concept arriving early. Welcomed.

## Heads up about Week 3

- Reading: Manning Ch 2 (tensors, gradients, SGD/backprop). It's the heaviest math week in the pilot — "just enough to debug."
- We'll reproduce a tiny model partially from scratch and run a controlled experiment on learning rate or batch size.
- The Week 2 spike rhythm continues. Sacred Flow continues for Code Builders.

## Where to go next

→ Week 3 (not yet built — this is where we stop for the vertical-slice pass).
