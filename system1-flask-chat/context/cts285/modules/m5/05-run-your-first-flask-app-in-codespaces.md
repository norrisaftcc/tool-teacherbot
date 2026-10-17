CTS-285 • Module 5

## M5.3 — Run Your First Flask App in Codespaces

You have tested Flask responsibilities in controlled simulations. Now run a small real Flask application in Codespaces and inspect the same boundaries in working code.

Implementation target

**Run → inspect → change one responsibility → test again → commit what you learned.**

### Get the controlled starter

The student starter keeps the same three responsibilities you have been analyzing:

- `app.py` — Flask routes and request/response coordination;
- `business_logic.py` — reusable two-attempt behavior;
- `data_store.py` — a deliberately simple temporary state boundary;
- `templates/index.html` — the browser-facing interface.

[Get the Minimal Flask Starter](https://amlw05.github.io/cts-285-course-simulations/m5/flask-starter/)

Download the starter files from the resource page and place them in a clearly named Module 5 folder in **your own CTS-285 repository**. Keep the folder structure shown on the resource page.

**That folder is your project root.** Every command on this page runs from it. Module 6 and Module 7 use the same folder and call it by the same name. Module 6 asks you to add a `tests/` folder inside it. Do not move the application after this point.

**Your `docs/` folder is different, and it does not move.** It stays at the top level of your repository, where it has been since Module 2. It already holds `docs/requirements.md` and `docs/product-backlog.md`. Module 7 adds `docs/schema.md` there, beside them, not inside the project root.

### 1. Run it

Open your repository in Codespaces, move into the starter folder, and run:

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m flask --app app run --debug --host=0.0.0.0
```

Open the forwarded port when Codespaces offers it. You should see a small DataMan Answer Checker.

The first two commands make a virtual environment and switch to it. The environment keeps this project's Flask separate from everything else on the machine. You make it once. A fresh terminal starts without it, so run `source .venv/bin/activate` again before anything else in that terminal.

`python3` creates the environment, because the environment does not exist yet. `python` does everything after that, because it is the interpreter inside the environment you just activated. Every later module follows the same rule.

### 2. Establish the baseline

1. Submit one wrong answer. The app should allow another try.
2. Submit another wrong answer. The app should reveal the correct answer.
3. Restart the app to reset its temporary state.

If the baseline does not behave as expected, stop and inspect the request flow before changing code. A change is meaningful only when you know what behavior existed before it.

### 3. Trace one request through the files

Follow a submitted answer from beginning to end:

**Form**
submitted answer

**app.py**
receive + coordinate

**business_logic.py**
apply rule

**data_store.py**
preserve state

**Template**
show outcome

### 4. Make one controlled change

Change the user-facing retry message from `Try again.` to a different clear message appropriate for a learner.

**Constraint:** make the change where that product outcome is decided. Do not hard-code a replacement message into the HTML template just because that is where the message appears.

Run the same wrong-answer path again. Verify that the new response appears and that the two-attempt behavior still works.

### 5. Ask one harder question

The current data store is intentionally temporary. Its state exists only while the Python process stays alive. Ask:

**What would break if the process restarted between the learner's first and second attempt?**

Do not solve persistence yet. Identify the information the final implementation would need to preserve so the acceptance criterion remains true.

### 6. Leave evidence in GitHub

Commit your controlled change with a descriptive message. Your commit should make clear what changed and why.

**Before you continue, you should be able to show:**

- a running Flask application in Codespaces;
- the request path across the framework, logic, state, and template boundaries;
- one controlled change made in the correct responsibility layer;
- the same behavior retested after the change;
- a Git commit that records the change.

**Nothing is submitted in Canvas here.** The working repository and commit are your persistent evidence. Next, you will prepare your own M4 product slice for migration into this Flask structure.
