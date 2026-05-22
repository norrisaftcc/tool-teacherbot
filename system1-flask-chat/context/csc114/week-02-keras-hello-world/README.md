# Week 2 — Keras hello world

**Pilot week:** 2 of 8 (CSC-114 Summer 2026)
**Theme:** From "what is an agent" to "what is a neural network." This week you train a real model with real numbers, and you set up the workflow you'll use for the rest of the term.
**Manning chapter(s):** Ch 1 (what deep learning is) + Ch 4 (classification and regression). Reading is assigned.

---

## What changes from Week 1

Two things, and they matter:

1. **Sacred Flow starts for the Code Builders track.** Issue → branch → PR → merge becomes the way Code Builders submit work. Prompt Masters keep submitting by drop. We deliberately split tracks here so that students without a CSC-113 ramp-up aren't drowning in `git` on Day 8 of the course.
2. **Textbook reading is now real.** Before Meeting A, you should have skimmed Manning Ch 1; before Meeting B, Ch 4 §1–2. We're not going to lecture the textbook back to you in class.

## Learning outcomes

By Friday, you can:

1. **Explain** what a neural network is at the "tensors flow through layers and weights update" level — not the math, the *mechanics*.
2. **Load** a standard dataset (MNIST) via Keras.
3. **Build** a minimal `Sequential` model: input → dense → dense → output.
4. **Train** it with `.fit()`, evaluate it with `.evaluate()`, predict with `.predict()`.
5. **Read** a training curve and identify whether your model is underfit, overfit, or just-right.
6. **Write up** a baseline metric + one paragraph of error analysis ("what fails, what might help").

## What you do this week

1. **[learn.md](learn.md)** — *Manning Ch 1 + Ch 4 framing.* Concepts. Read before Meeting A.
2. **[practice.md](practice.md)** — *Hello, training loop.* Retry-OK. Load MNIST, build a `Sequential`, fit it, look at the loss curve.
3. **[apply.md](apply.md)** — *Your first spike prototype.* Baseline metric + error analysis. One narrow experiment.
4. **[assess.md](assess.md)** — *What you submit, split by track.*

## Two-track expectations this week

**Sacred Flow starts here for Code Builders.** Same artifact, two paths.

| Track | Submit by | Process artifacts |
|---|---|---|
| Code Builders | Open a GitHub Issue (`Week 2 spike: <your one-line description>`) → branch off `main` named `week2-yourname` → commit notebook + write-up → open PR → request review → merge after at least one comment. PR description contains a 1-paragraph **retro** ("what worked, what surprised me, what I'd do differently"). | Issue + branch + PR + retro |
| Prompt Masters | Add the same notebook + write-up to your repo via GitHub Desktop or the web "add file" button. | None — just the artifact |

Both tracks earn identical points on the *artifact*. Code Builders earn **process credit** for the issue/PR/retro on top.

## Before you start

- [ ] Manning *Deep Learning with Python*, 3rd ed., available (book, library, e-book — your call).
- [ ] Python 3.10+ with `pip` working, OR a Google Colab account. **Keras + TensorFlow** must be reachable.
- [ ] The textbook's notebook companion cloned or visible: `planning/textbook/deep-learning-with-python-notebooks-master/`. We reference these directly — don't duplicate the code into our materials.
- [ ] (Code Builders only) `git` working from your terminal, OR GitHub Desktop installed.

If your environment isn't ready, fix that *first*. The Sacred Flow Lab from CSC-113 (at `planning/csc_dash/CSC-114/activities/Module_01_Sacred_Flow_Lab.md`) covers Python + venv + Jupyter setup in detail. We've adapted the ML model section for Keras; the environment setup section is unchanged.

## Source material this week draws from

- **Primary student reading:** Manning Ch 1, Ch 4. The companion notebook is `planning/textbook/deep-learning-with-python-notebooks-master/chapter04_classification-and-regression.ipynb`.
- **Practice slot adapted from:** `planning/csc_dash/CSC-114/activities/Module_01_Sacred_Flow_Lab.md` (we swap sklearn-Iris → Keras-MNIST).
- **Vocabulary reference (optional):** `planning/csc_dash/CSC-114/knowledge-checks/Module_01_Knowledge_Check.md`.
