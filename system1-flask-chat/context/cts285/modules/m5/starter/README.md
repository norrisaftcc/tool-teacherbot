# Minimal DataMan Flask Starter

Purpose: controlled first Flask implementation for CTS-285 Module 5.

This starter keeps three responsibilities visible:

- `app.py` — Flask/interface coordination
- `business_logic.py` — reusable DataMan rule behavior
- `data_store.py` — deliberately simple state boundary
- `templates/index.html` — user-facing response

## Run in Codespaces

From this folder, which is your project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m flask --app app run --debug --host=0.0.0.0
```

Open the forwarded port when Codespaces prompts you.

You make the environment once. A fresh terminal starts without it, so run
`source .venv/bin/activate` again before anything else in that terminal.

`python3` creates the environment, because it does not exist yet. `python` does
everything after that, because it is the interpreter inside the environment you
just activated.

## Controlled test

1. Submit a wrong answer once. Expected: `Try again.`
2. Submit a wrong answer a second time. Expected: correct answer revealed.
3. Restart the app to reset the in-memory state.
4. Make the controlled change named on the Canvas page.
5. Run the same behavior again and inspect what changed.

This starter is instructional scaffolding, not the final DataMan architecture. The in-memory store is intentionally temporary so students can see the data/state boundary before introducing a database.
