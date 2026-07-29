> **HISTORICAL — do not act on this file.** It describes a project shape
> (five capstone groups, two parallel systems) that the code stopped
> matching in July 2026. Kept as a paper trail. For what is actually
> true, read `docs/adr/`, `docs/registry/KEEP.md`, and
> `system1-flask-chat/DEPLOY.md`.
>
> Paths in the body still read `docs/plans/`. That directory was folded into
> `docs/historical/plans/` in July 2026. The body is left as written, because it
> records what was observed at the time, not where the files live now.

The "MVP" claim is suspect — the `system1-flask-chat/` directory only has `models.py`, a requirements file, and one test module. Let me read the design docs and what exists to confirm.

Now I have the spec. Let me read what was actually implemented and the design guidelines in parallel.

Let me also confirm there's no unmerged branch with more MVP work on GitHub.

Quick check on the two "ready" docs that name-suggest the MVP is done.

I have the full picture. The "MVP is up" claim doesn't match what's in the repo. Here's the punch list.

---

## Headline

**The MVP is not up.** Only Task 2 of the 9-task implementation plan (`docs/plans/2026-05-12-system1-implementation.md`) has actually shipped — `models.py` + its tests. Everything user-facing (routes, auth, Claude integration, templates, JS) is unwritten. The test suite as committed cannot even run.

## ✅ Done

| Item | Notes |
|---|---|
| `requirements.txt` | Matches spec verbatim |
| `.env.example` | Matches spec verbatim |
| `models.py` (Group / Conversation / Message) | Implements spec; `increment_tokens` clamps at `token_budget` (improvement beyond spec, covered by test) |
| `tests/test_models.py` | 5 tests including the budget-clamp case |
| `tests/__init__.py`, `tests/conftest.py` | Files exist (but see Critical below) |
| Design tokens authored | `design/system1/colors_and_type.css` + `kit.css` are the new source of truth; `docs/design/design-guidelines.md` updated to point at them |

## 🟡 Partial

- **Test scaffolding** — only `test_models.py` exists. Spec calls for `test_app.py`, `test_auth.py`, `test_claude_handler.py`, `test_routes.py`. None present.
- **Design pipeline** — JSX/CSS mockups delivered, but no translation into Jinja templates exists yet, and the implementation plan (Task 7, lines 891-924) still falls back to the abandoned `#00ff41` green-on-black palette that `design-guidelines.md` explicitly tells you *not* to use.

## ❌ Missing

Everything that makes it a web app:

- `app.py` (Flask factory) — Tasks 3
- `routes.py` (login, logout, /chat page, /api/chat JSON, /admin, /admin login) — Tasks 3, 4, 6
- `auth.py` (5-group credential dict, `load_group_context`) — Task 4
- `claude_handler.py` (system prompt builder, Anthropic call) — Task 5
- `templates/` — all four templates (`login.html`, `chat.html`, `admin.html`, `admin_login.html`)
- `static/css/terminal.css` and `static/js/chat.js`
- `context/group_N_context.md` files for the 5 groups
- `render.yaml` — Task 9

## 🚨 Critical — test suite cannot run as committed

`tests/conftest.py:2` does `from app import create_app`. `app.py` does not exist. Pytest collection of `test_models.py` requires the `app` fixture, so **`pytest` will fail at import for every existing test**. The models tests have never been runnable in this committed state. Either the tests were green pre-conftest and never re-run, or this slipped past whoever committed `ef7402d`. First thing to do if you continue here: stub `app.py` with a minimal factory so the green tests turn green again.

## ❓ Unclear / spec ambiguities

1. **Two different sets of group credentials in the repo.**
   - `docs/plans/2026-05-12-system1-implementation.md` (Task 4): `group1/capstone2026`, `group2/dataman2026`, `group3/finaid2026`, `group4/health2026`, `group5/sched2026` — groups numbered 1–5.
   - `LAUNCH_READY.md`: `group0/obag2026`, `group1/steered2026`, `group2/biosync2026`, `group3/studystream2026`, `group4/datamon2026` — groups numbered 0–4, totally different passwords and projects.
   Spec needs a single source of truth before `auth.py` gets written.

2. **Anthropic SDK is years out of date for the target model.** `requirements.txt` pins `anthropic==0.18.0` (Feb 2024). The implementation plan's `claude_handler.py` (line 619) calls `model='claude-sonnet-4-6'`, which won't be a valid model id on a 0.18 SDK. Bump to a recent SDK before testing the chat path.

3. **Flask-Login is required but the spec then bypasses it.** Task 4 admits Flask-Login's `login_user` needs a UserMixin, and switches to a custom `@group_login_required` session decorator. So `flask-login==0.6.3` is in `requirements.txt` and `login_manager.init_app(app)` is in `app.py` for no reason. Decide: real Flask-Login or pure session.

4. **Admin auth is `?password=X` in the query string** (spec, Task 6). Spec acknowledges this is alpha-grade. Worth replacing with a POST form + session flag before any classroom use — query strings get logged, leaked via Referer, and cached in browser history.

5. **Per-conversation logic is ambiguous.** Planned `api_chat` (lines 818-824) treats "client-provided history is empty" as "start a new Conversation". A page refresh therefore silently starts a new conversation row. Two students in the same group also interleave into one Conversation. Decide whether `Conversation` is scoped per-group, per-browser-session, or per-student — the data model doesn't enforce any of these.

6. **Token budget has a race condition.** Budget check happens before the API call; `increment_tokens` happens after. Two concurrent requests can both pass the gate and both increment past the budget. `increment_tokens` clamps in Python but the read-modify-write isn't atomic across requests.

7. **No CSRF protection** on `/login` or `/api/chat`. `WTF_CSRF_ENABLED: False` is set in `conftest.py`, but `flask-wtf` isn't in requirements anyway — so CSRF was never enabled in the production path. Probably fine for an alpha behind a class roster, but flag explicitly.

8. **Design guidelines vs design doc disagree on palette.** `docs/plans/2026-05-12-system1-design.md` line 146 still says "green primary text". `docs/design/design-guidelines.md` says cream-on-navy and explicitly forbids the green palette. The design doc needs a follow-up edit, or future readers will get whiplash.

## 🧪 Testing scaffolding — what exists vs what's needed to validate the MVP

| Layer | Exists | Needed |
|---|---|---|
| Models | ✅ 5 tests | (good) |
| App factory | — | `test_app.py` (factory boots, `/` reachable, `/chat` redirects unauthed) |
| Auth | — | `test_auth.py` (valid/invalid creds, missing-context-file failure, logout clears session) |
| Claude handler | — | `test_claude_handler.py` (system prompt contains context + pedagogical rules; response parsing; mocked SDK call) |
| Routes / integration | — | `test_routes.py` (login flow, `/api/chat` 200/403/502 paths, admin gate) |
| End-to-end smoke | — | A manual browser walkthrough is in the plan (Task 7 Step 4) — no Playwright/Selenium scaffolding planned |
| CI | — | No GitHub Actions / pre-commit config exists |
| Conftest is broken | 🚨 | Fix `from app import create_app` before any of the above will run |

## Suggested next moves

1. Reconcile the credentials/group conflict (#1).
2. Stub `app.py` + `routes.py` so `pytest` collects — even an empty factory unblocks the existing model tests.
3. Bump the `anthropic` SDK pin before writing `claude_handler.py` (#2).
4. Update the design doc's "green primary text" line to defer to `design-guidelines.md` (#8).
5. Then resume the plan at Task 3.

Want me to start on any of these? The reconciliation in #1 is a question for you; the rest I can do.