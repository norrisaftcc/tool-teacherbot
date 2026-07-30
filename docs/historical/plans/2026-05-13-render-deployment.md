# Render Deployment — System 1 Implementation Plan

> **SUPERSEDED — do not act on this document.**
>
> A May 2026 plan for a stack that no longer exists. It provisions free-tier
> Render resources under names (`teacherbot-db`) that were replaced by the Pro
> Blueprint in `render.yaml`, and the database it describes has since been
> deleted. It also predates Alembic (ADR-0006), so any schema reasoning in it is
> wrong.
>
> It is kept for the reasoning, not the steps. Current operator truth is
> `system1-flask-chat/DEPLOY.md`; current decisions are `docs/registry/KEEP.md`.
>
> This banner exists because the file is written as executable steps. It used to
> open with a directive telling an agent to work through it task-by-task; that
> directive was struck in July 2026 (K19), because a superseded document whose
> first line is an imperative gets acted on before the banner is read.

> **SUPERSEDED by `docs/historical/plans/2026-05-16-render-deployment.md`.**
> MCP tools assumed by this plan are not available. See the 2026-05-16 plan
> for the CLI+REST approach actually used.

> *Steps use `- [ ]` checkboxes. This was written for task-by-task execution by an
> agent; it records how the work was sequenced, not how to sequence work now.*

**Goal:** Deploy `system1-flask-chat` to Render as a Python web service backed by a managed PostgreSQL database.

**Architecture:** Create a fresh PostgreSQL instance and web service via the Render MCP tools, passing all configuration inline. The `rootDir` limitation in the MCP API is worked around by prefixing build/start commands with `cd system1-flask-chat &&`. Environment variables (API key, secret key, admin password, database URL) are set on the service after the postgres connection string is known.

**Tech Stack:** Render MCP tools, Flask/Gunicorn, PostgreSQL (Render managed), Anthropic API.

---

## MCP Tool Constraints (read first)

- No delete-service tool exists — `tool-teacherbot` must be removed manually from the Render dashboard after this plan completes.
- `create_web_service` and `update_web_service` do not accept a `rootDir` parameter — use `cd system1-flask-chat &&` prefix instead.
- `update_web_service` schema exposes no update fields via MCP — use `update_environment_variables` for post-creation changes.

---

## Task 1: Generate secret values

**Purpose:** Prepare the three secret env vars needed before creating the service.

- [ ] **Step 1: Generate FLASK_SECRET_KEY**

  Run in terminal:
  ```bash
  python3 -c "import secrets; print(secrets.token_hex(32))"
  ```
  Copy the output — this is your `FLASK_SECRET_KEY`.

- [ ] **Step 2: Confirm ANTHROPIC_API_KEY**

  Retrieve your key from https://console.anthropic.com/settings/api-keys.
  Have it ready as a string starting with `sk-ant-`.

- [ ] **Step 3: Choose ADMIN_PASSWORD**

  Pick a password for the `/admin` dashboard. Something memorable but not reused.
  Example: `algocratic-admin-2026`

---

## Task 2: Create the PostgreSQL database

**MCP tool:** `mcp__render__create_postgres`

- [ ] **Step 1: Create the database**

  Call `mcp__render__create_postgres` with:
  ```json
  {
    "name": "algocratic-ta-db",
    "plan": "free",
    "region": "virginia",
    "version": 16
  }
  ```

- [ ] **Step 2: Extract the connection string**

  From the response, find the `connectionString` (or `externalConnectionString`) field. It will look like:
  ```
  postgresql://<auto-user>:<password>@<host>/<auto-dbname>
  ```
  > Note: The MCP API does not accept custom `databaseName` or `user` params — Render generates these automatically. The connection string in the response is the authoritative value; use it verbatim as `DATABASE_URL`.

  Save this — it becomes `DATABASE_URL` in Task 3.

  > Note: Render free-tier postgres takes 1-2 minutes to provision. Wait until status is `available` before proceeding.

---

## Task 3: Create the web service

**MCP tool:** `mcp__render__create_web_service`

- [ ] **Step 1: Create the service with all env vars inline**

  Call `mcp__render__create_web_service` with:
  ```json
  {
    "name": "algocratic-ta-system1",
    "runtime": "python",
    "repo": "https://github.com/norrisaftcc/tool-teacherbot",
    "branch": "main",
    "buildCommand": "cd system1-flask-chat && pip install -r requirements.txt",
    "startCommand": "cd system1-flask-chat && gunicorn \"app:create_app()\"",
    "region": "virginia",
    "plan": "free",
    "autoDeploy": "yes",
    "envVars": [
      { "key": "ANTHROPIC_API_KEY",  "value": "<your-sk-ant-key>" },
      { "key": "FLASK_SECRET_KEY",   "value": "<output-from-task-1-step-1>" },
      { "key": "ADMIN_PASSWORD",     "value": "<chosen-password>" },
      { "key": "DATABASE_URL",       "value": "<connection-string-from-task-2-step-2>" }
    ]
  }
  ```

- [ ] **Step 2: Record the service ID**

  From the response, save `id` (format: `srv-...`). Needed for any follow-up MCP calls.

- [ ] **Step 3: Record the service URL**

  From the response, save `serviceDetails.url` — will be:
  `https://algocratic-ta-system1.onrender.com`

---

## Task 4: Monitor the initial deploy

**MCP tool:** `mcp__render__list_deploys`

- [ ] **Step 1: Check deploy status**

  Call `mcp__render__list_deploys` with the service ID from Task 3.
  Wait until the most recent deploy shows `status: live`.

  > Free-tier cold starts take 3-5 minutes for initial build + deploy. Check every 60 seconds.

- [ ] **Step 2: Check deploy logs if status is `failed`**

  Call `mcp__render__list_logs` with the service ID.
  Common failure causes:
  - Wrong build command path → verify `cd system1-flask-chat &&` prefix
  - Missing env var → check `DATABASE_URL` is a valid `postgresql://` URL (not `postgres://`)
  - `ModuleNotFoundError` → requirements.txt not found, path issue

---

## Task 5: Verify the running application

- [ ] **Step 1: Check the login page**

  ```bash
  curl -s -o /dev/null -w "%{http_code}" https://algocratic-ta-system1.onrender.com/
  ```
  Expected: `200`

- [ ] **Step 2: Test group login**

  In a browser, navigate to `https://algocratic-ta-system1.onrender.com/`
  - Group ID: `group1`
  - Password: `capstone2026`

  Expected: redirect to `/chat`

- [ ] **Step 3: Send a test chat message**

  In the chat interface, send: `Hello, what project is my team working on?`
  Expected: streamed response from Claude (text appears token by token)

- [ ] **Step 4: Verify admin dashboard**

  Navigate to:
  `https://algocratic-ta-system1.onrender.com/admin?password=<ADMIN_PASSWORD>`
  Expected: admin page showing groups and (after step 3) at least one conversation logged.

---

## Task 6: Clean up old service

- [ ] **Step 1: Delete the misconfigured service from the dashboard**

  Visit: https://dashboard.render.com/web/srv-d81rsrv7f7vs73eeihmg
  Go to Settings → Delete Service.

  > There is no delete-service MCP tool. This is a manual step.

---

## Post-Deployment: Fill in group context files

The app works but Claude has no real project context for any group yet. All five context files are placeholder templates.

- [ ] **Step 1: Edit each context file in the repo**

  Files to fill in:
  - `system1-flask-chat/context/group1_context.md` (Group 1 / capstone2026)
  - `system1-flask-chat/context/group2_context.md` (Group 2 / dataman2026)
  - `system1-flask-chat/context/group3_context.md` (Group 3 / finaid2026)
  - `system1-flask-chat/context/group4_context.md` (Group 4 / health2026)
  - `system1-flask-chat/context/group5_context.md` (Group 5 / sched2026)

  Replace `[INSTRUCTOR: fill in]` placeholders with real project details, tech stack, current sprint, team members.

- [ ] **Step 2: Commit and push — auto-deploy will pick it up**

  ```bash
  git add system1-flask-chat/context/
  git commit -m "chore: fill in group context files for alpha"
  git push origin main
  ```

  Render will redeploy automatically (usually 2-3 minutes).
