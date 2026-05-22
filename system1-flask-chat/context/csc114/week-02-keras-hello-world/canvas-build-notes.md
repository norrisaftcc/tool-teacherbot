# Canvas build notes — Week 2

How to import this week's Knowledge Check and overview page into Canvas, and how to rebuild the quiz import file if the source changes.

This file is for **instructors**, not students.

---

## Files in this folder

| File | What it is | What to do with it |
|---|---|---|
| `canvas-page.html` | Paste-into-Canvas overview page for Week 2. | See "Import the overview page" below. |
| `knowledge-check.md` | text2qti source for the 13-question Knowledge Check. | Edit when questions need to change; rebuild the zip. |
| `knowledge-check.zip` | Generated QTI 1.2 package. | Import into Canvas Classic Quizzes. |

The `.zip` is rebuilt from the `.md`. The `.md` is the source of truth; if you find a typo or want to change a question, edit the `.md` and rebuild.

---

## Import the Knowledge Check (QTI zip → Canvas Classic Quiz)

1. In your Canvas course, go to **Settings → Import Course Content**.
2. **Content Type:** "QTI .zip file".
3. **Source:** upload `knowledge-check.zip`.
4. Leave "Default Question Bank" empty (the import creates its own).
5. Click **Import**. The import shows up under the "Current Jobs" section — wait until it says "Completed".
6. The new quiz appears under **Quizzes → All Quizzes** (Classic Quizzes section). It is **unpublished** by default. Open it, set point values and a due date if needed, then **Publish**.
7. **Capture the quiz ID** from the URL (`.../courses/<COURSE_ID>/quizzes/<QUIZ_ID>`). You'll need it when importing the overview page.

> **About New Quizzes:** Canvas's newer "New Quizzes" engine uses QTI 2.1, not 1.2. text2qti currently produces 1.2, which lands in Classic Quizzes. If your institution has fully migrated to New Quizzes, use Canvas's "Migrate" tool inside Quizzes to convert the imported Classic Quiz, or recreate the quiz manually with the source markdown as a reference.

---

## Import the overview page (HTML → Canvas Page)

1. In Canvas, go to **Pages → + Page**.
2. Title it: `Week 2 — Keras Hello World` (or whatever your course's naming convention is).
3. Switch the editor to **HTML view** (the `<>` icon, sometimes labeled "HTML Editor").
4. Open `canvas-page.html` in a text editor, **select all**, copy.
5. Paste into the Canvas HTML editor. Switch back to rich text view to confirm the layout looks right.
6. **Replace placeholders.** Search the page for these tokens and swap each one:
   - `[COURSE_ID]` → your course's numeric Canvas ID (visible in any Canvas URL).
   - `[ASSIGNMENT_ID]` → the numeric ID of the Week 2 Assess assignment (after you create it).
   - `[FILE_ID]` → the numeric ID of any uploaded files (e.g., learn.md, practice.md, apply.md uploaded to Canvas Files). If you'd rather link to the GitHub source, replace with a direct GitHub URL instead.
   - `[QUIZ_ID]` → the quiz ID you captured from the import step above.
7. **Save & Publish** the page.

---

## Rebuild the quiz zip when the source changes

If you edit `knowledge-check.md` (fixing a typo, swapping a question, rewording an explanation), regenerate the zip:

```bash
# Run from the repo root:
cd planning/pilot_su26/week-02-keras-hello-world
../../../.venv/bin/text2qti knowledge-check.md
```

Outputs:
- `knowledge-check.zip` — the new QTI package (overwrites the previous one).

If you'd also like a human-readable answer key for proofreading, add `--solutions`:

```bash
# Run from inside the week-02 folder (after the cd above), or from the repo root prefixed by `cd planning/pilot_su26/week-02-keras-hello-world &&`:
../../../.venv/bin/text2qti --solutions knowledge-check.md
```

This produces `knowledge-check_solutions.html` alongside the zip. **Do not commit it** — it's reviewer-only.

Commit the new `.zip` alongside the `.md` change:

```bash
git add knowledge-check.md knowledge-check.zip
git commit -m "rebuild Week 2 KC: <what changed>"
```

When you re-import the zip into Canvas, Canvas treats it as a **new quiz** by default — the old quiz is not updated in place. Either delete the old quiz first, or accept the duplicate and unpublish the old one. There is no clean "update existing quiz from QTI" path in Classic Quizzes; this is a Canvas limitation.

---

## Install / dependencies

text2qti is a Python package that requires pandoc on PATH. We install it into a project-local virtual environment so it doesn't conflict with any system Python.

```bash
# pandoc (one time, system-wide) — use whichever applies to your OS:
brew install pandoc                # macOS
sudo apt-get install pandoc        # Linux (Debian/Ubuntu)

# Project venv + text2qti (from the repo root)
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install text2qti

# Verify
.venv/bin/text2qti --version
```

The `.venv/` directory is gitignored. Each clone of the repo needs to run these install steps once.

If `.venv/bin/text2qti --version` prints a version, you're set.

---

## Troubleshooting

- **`text2qti` fails to parse the source.** Most common cause: missing blank lines between questions, or a question that doesn't start with a number and a dot (`1.`, `2.`, etc.). Check the file's exact formatting against a known-good question in `knowledge-check.md`.
- **`pandoc not found`** at build time: install pandoc (see "Install / dependencies" above). text2qti uses pandoc to render markdown inside question stems.
- **Canvas import says "no questions found".** Canvas occasionally rejects QTI zips that contain a `__MACOSX/` folder. text2qti shouldn't produce one, but if you find one in the zip (`unzip -l knowledge-check.zip`), regenerate the zip from a non-macOS environment or remove the folder with `zip -d`.
- **Imported quiz has questions but no points.** That's expected — set point values in Canvas after import. text2qti doesn't specify points per question.
