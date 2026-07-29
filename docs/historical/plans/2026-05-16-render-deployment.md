# Render Deployment Implementation Plan — Revision 2

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
>
> Paths in the body still read `docs/superpowers/`. That directory was folded
> into `docs/historical/` in July 2026. The body is left as written, because it
> records what the plan instructed at the time, not where the files live now.

> *Steps use `- [ ]` checkboxes. This was written for task-by-task execution by an
> agent; it records how the work was sequenced, not how to sequence work now.*

**Goal:** Deploy `system1-flask-chat/` to Render as a Python web service named `teacherbot` backed by a managed Postgres DB `teacherbot-db`. Delete the old misconfigured `tool-teacherbot` service before creating the new one. Land a PR with deploy config + operator docs first; then drive the actual provisioning via Render CLI plus targeted REST calls.

**Architecture:** Two-phase. **Phase A** (Tasks 1–8) is repo-side: branch, doc updates, render.yaml fix, operator runbook, PR linked to a tracking issue, merge to `main`. **Phase B** (Tasks 9–18) is cloud-side: REST `DELETE` the old service, REST `POST` to create the Postgres DB, fetch its connection string, CLI `render services create` for the web service with all env vars inline, wait for the deploy, run HTTP smoke tests, hand off to the user for a browser smoke test, prove auto-deploy with a no-op commit, close the issue with a command-trail comment.

**Tech Stack:** Render CLI v2.17.0, Render REST API (`https://api.render.com/v1/`), `gh` CLI, `git`, `curl`, `jq`, Flask/Gunicorn, PostgreSQL.

**Supersedes:** `docs/historical/plans/2026-05-13-render-deployment.md`

---

## Pre-flight: confirm environment

These are not formal tasks but must be true before starting Task 1.

- Working directory: `/Users/norrisa/Documents/dev/github/tool-teacherbot`
- Git branch: `system1/deploy-render` (already created and contains the design spec from 2026-05-16)
- `render --version` returns `v2.17.0` or newer
- `render whoami` returns the user's email
- `render workspace set tea-d81rjp0sfn5c738tl430` has been run at least once in this shell or earlier
- `gh auth status` returns logged in
- `RENDER_API_KEY` is exported in the user's shell (only required at start of Phase B)

If any of the above is false, stop and resolve it before continuing.

---

# Phase A — Repo changes (the PR)

## Task 1: Capture old plan/spec as superseded

**Purpose:** Leave a paper trail. The 2026-05-13 docs are still valid history, but anyone reading them needs to know they no longer describe the current approach.

**Files:**
- Modify: `docs/superpowers/specs/2026-05-13-render-deployment-design.md` (banner at top)
- Modify: `docs/superpowers/plans/2026-05-13-render-deployment.md` (banner at top)

- [ ] **Step 1: Add SUPERSEDED banner to the 2026-05-13 spec**

  Open `docs/superpowers/specs/2026-05-13-render-deployment-design.md`. Immediately after the YAML frontmatter (the second `---`) and before the existing `# Render Deployment Design` heading, insert this block:

  ```markdown
  > **SUPERSEDED by `docs/superpowers/specs/2026-05-16-render-deployment-design.md`.**
  > This document assumed Render MCP tools that were not available in the agent
  > environment. The 2026-05-16 revision drives the deploy via Render CLI plus
  > targeted REST calls and renames the service to `teacherbot`.
  ```

- [ ] **Step 2: Add SUPERSEDED banner to the 2026-05-13 plan**

  Open `docs/superpowers/plans/2026-05-13-render-deployment.md`. Insert this block as the second line of the file (immediately after the `# Render Deployment — System 1 Implementation Plan` heading):

  ```markdown

  > **SUPERSEDED by `docs/superpowers/plans/2026-05-16-render-deployment.md`.**
  > MCP tools assumed by this plan are not available. See the 2026-05-16 plan
  > for the CLI+REST approach actually used.
  ```

- [ ] **Step 3: Verify no other file references the old plan as current**

  Run:
  ```bash
  grep -rn "2026-05-13-render-deployment" --include='*.md' .
  ```
  Expected: only the two files just edited, plus the new spec/plan that explicitly mark them as superseded. No README pointer, no CLAUDE.md reference. If any other reference exists, update it to point at the 2026-05-16 doc.

- [ ] **Step 4: Commit**

  ```bash
  git add docs/superpowers/specs/2026-05-13-render-deployment-design.md \
          docs/superpowers/plans/2026-05-13-render-deployment.md
  git commit -m "$(cat <<'EOF'
  docs: mark 2026-05-13 Render deploy spec + plan as superseded

  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  EOF
  )"
  ```

---

## Task 2: Audit and fix `render.yaml`

**Purpose:** Keep the Blueprint file consistent with what we actually deploy. If someone later runs "New Blueprint" against this repo, it should produce the same teacherbot/teacherbot-db pair, not the old `algocratic-ta-system1` / `algocratic-ta-db` names with custom `databaseName`/`user`.

**Files:**
- Modify: `render.yaml`

- [ ] **Step 1: Read the current file**

  ```bash
  cat render.yaml
  ```
  Confirm the existing content matches what is shown in the diff below before editing.

- [ ] **Step 2: Replace `render.yaml` with the corrected version**

  Overwrite `render.yaml` with:

  ```yaml
  services:
    - type: web
      name: teacherbot
      env: python
      rootDir: system1-flask-chat
      buildCommand: pip install -r requirements.txt
      startCommand: gunicorn "app:create_app()"
      autoDeploy: true
      envVars:
        - key: ANTHROPIC_API_KEY
          sync: false
        - key: FLASK_SECRET_KEY
          sync: false
        - key: ADMIN_PASSWORD
          sync: false
        - key: DATABASE_URL
          fromDatabase:
            name: teacherbot-db
            property: connectionString

  databases:
    - name: teacherbot-db
      plan: free
  ```

  Changes vs. the prior file:
  - `name: algocratic-ta-system1` → `name: teacherbot`
  - DB `name: algocratic-ta-db` → `name: teacherbot-db`
  - Removed `databaseName: ta_system` and `user: ta_admin` (CLI-created DB will use Render-assigned values, and a future Blueprint should match the running cloud state)
  - Added `autoDeploy: true` (was implicit; making it explicit matches what we set via CLI)
  - Added `plan: free` to the database stanza (was missing; explicit is better than implicit)

- [ ] **Step 3: Validate the YAML with the Render CLI**

  ```bash
  render blueprints validate render.yaml
  ```
  Expected: a green/success message and no validation errors. If the CLI reports errors, fix them inline before continuing.

- [ ] **Step 4: Commit**

  ```bash
  git add render.yaml
  git commit -m "$(cat <<'EOF'
  fix(render): rename to teacherbot/teacherbot-db, drop custom DB params

  Aligns render.yaml with what the deploy will actually create. Custom
  databaseName and user were unsupported by the API path we use; removing
  them keeps the Blueprint reproducible.

  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  EOF
  )"
  ```

---

## Task 3: Write the operator runbook

**Purpose:** A future operator (or you, in three months) needs to know how this service was deployed, where its env vars live, how to read logs, and how to roll back. Lives next to the app, not buried in `docs/superpowers/`.

**Files:**
- Create: `system1-flask-chat/DEPLOY.md`

- [ ] **Step 1: Write the runbook**

  Create `system1-flask-chat/DEPLOY.md` with the following content:

  ````markdown
  # System 1 — Render Deployment Runbook

  This document describes how `teacherbot` is deployed on Render and how to
  operate it. The deploy was originally provisioned by a one-time bootstrap
  procedure documented in `docs/superpowers/plans/2026-05-16-render-deployment.md`.

  ## Service summary

  | Property | Value |
  |---|---|
  | Service name | `teacherbot` |
  | Database name | `teacherbot-db` |
  | Region | Virginia (us-east) |
  | Plan | free (web + DB) |
  | Branch deployed | `main` |
  | Root directory | `system1-flask-chat` |
  | Auto-deploy | enabled (every push to `main`) |
  | Service URL | recorded in tracking issue at first deploy |

  ## Required environment variables

  | Variable | Source / how to set |
  |---|---|
  | `ANTHROPIC_API_KEY` | Instructor's key from https://console.anthropic.com/. Starts with `sk-ant-`. |
  | `FLASK_SECRET_KEY` | Generated random hex: `python3 -c "import secrets; print(secrets.token_hex(32))"`. Rotate on suspected leak. |
  | `ADMIN_PASSWORD` | Chosen string. Gates `/admin?password=…`. Alpha-grade auth — replace before public use. |
  | `DATABASE_URL` | Connection string from the `teacherbot-db` instance. `app.py:18-21` rewrites `postgres://` and `postgresql://` to `postgresql+psycopg://`. |

  Read or update env vars:

  ```bash
  # Read (requires RENDER_API_KEY)
  curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
    https://api.render.com/v1/services/<srv-id>/env-vars | jq .

  # Update one (without restarting):
  curl -s -X PUT \
    -H "Authorization: Bearer $RENDER_API_KEY" \
    -H "Content-Type: application/json" \
    -d '[{"key":"ADMIN_PASSWORD","value":"new-value"}]' \
    https://api.render.com/v1/services/<srv-id>/env-vars
  ```

  ## Common operations

  ### Find the service ID

  ```bash
  render workspace set tea-d81rjp0sfn5c738tl430   # one-time per shell
  render services --output json | jq -r '.[] | select(.service.name=="teacherbot") | .service.id'
  ```

  ### Trigger a manual deploy

  Auto-deploy fires on every push to `main`. To force one without a push:

  ```bash
  render deploys create <srv-id>
  ```

  ### Tail logs

  ```bash
  render logs --resources <srv-id>
  ```

  ### Roll back to a previous deploy

  ```bash
  render deploys list <srv-id> --output json | jq -r '.[] | "\(.deploy.id)  \(.deploy.status)  \(.deploy.commit.id[:7])"'
  # Pick a deploy ID with status=live from before the bad change:
  render deploys rollback <srv-id> --deploy-id <dep-...>
  ```

  > As of Render CLI v2.17.0, `deploys rollback` may not be available; if so,
  > use the dashboard's "Deploys" tab on the service: click the previous
  > successful deploy and press "Rollback".

  ### Suspend / resume the service

  ```bash
  # Suspend (free tier; DB is preserved):
  curl -s -X POST -H "Authorization: Bearer $RENDER_API_KEY" \
    https://api.render.com/v1/services/<srv-id>/suspend

  # Resume:
  curl -s -X POST -H "Authorization: Bearer $RENDER_API_KEY" \
    https://api.render.com/v1/services/<srv-id>/resume
  ```

  ### Restart the service (without redeploy)

  ```bash
  render restart <srv-id>
  ```

  ## Known alpha-grade issues

  These are documented in `current-status-report.md` and are out of scope for
  the initial deploy. File issues to track them before any production use:

  - Admin auth is `?password=...` query string. Replace with a POST login form.
  - No CSRF protection. `flask-wtf` is not in `requirements.txt`.
  - Token-budget enforcement has a race condition (read-modify-write between
    requests is not atomic).
  - `db.create_all()` runs on every startup; there is no migrations framework.

  ## Re-creating the service from scratch

  If `teacherbot` ever needs to be recreated, the canonical procedure is in
  `docs/superpowers/plans/2026-05-16-render-deployment.md`. The `render.yaml`
  Blueprint at the repo root is also a valid (though manual) starting point if
  you prefer the "New Blueprint" flow in the Render dashboard.
  ````

- [ ] **Step 2: Commit**

  ```bash
  git add system1-flask-chat/DEPLOY.md
  git commit -m "$(cat <<'EOF'
  docs: add System 1 operator runbook (DEPLOY.md)

  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  EOF
  )"
  ```

---

## Task 4: Add README pointer to the runbook

**Purpose:** Anyone arriving at the repo via README should be able to find the deploy docs without spelunking.

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Find the right insertion point**

  Run:
  ```bash
  grep -n "^## " README.md
  ```
  Identify the section that currently mentions deployment (likely "Deployment", "Tech Stack", or similar). If no such section exists, the pointer goes immediately before the LICENSE/credits section near the end.

- [ ] **Step 2: Insert the pointer**

  Add a short paragraph in the chosen section:

  ```markdown
  ### Deploying System 1

  System 1 is deployed to Render. The operator runbook (env vars, redeploy,
  logs, rollback) is at
  [`system1-flask-chat/DEPLOY.md`](system1-flask-chat/DEPLOY.md). The original
  bootstrap procedure is preserved at
  `docs/superpowers/plans/2026-05-16-render-deployment.md`.
  ```

  If a `## Deployment` heading already exists, place this under it. Otherwise add `## Deployment` and the paragraph above.

- [ ] **Step 3: Commit**

  ```bash
  git add README.md
  git commit -m "$(cat <<'EOF'
  docs(readme): point at System 1 deploy runbook

  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  EOF
  )"
  ```

---

## Task 5: Close the stale PR #1

**Purpose:** PR #1's branch is fully subsumed by `main`. Closing it removes confusion about which artifact represents current state.

- [ ] **Step 1: Verify PR #1 has no commits not on `main`**

  ```bash
  git fetch origin
  git log --oneline origin/main..origin/claude/add-teacherbot-demo-rKeS2
  ```
  Expected: a single commit (`0f983b7 feat(system1): runnable Flask demo with auth, chat, admin`). If this command shows more commits than that, stop and inspect — there may be unmerged work.

- [ ] **Step 2: Confirm that commit's contents are present on `main`**

  ```bash
  git log origin/main --oneline | grep -E "feat\(system1\): (auth module|app factory|Claude handler|chat API|full UI|streaming|Markdown)" | wc -l
  ```
  Expected: a number ≥ 5, indicating the work from the PR landed on main as separate commits.

- [ ] **Step 3: Close the PR with a comment**

  ```bash
  gh pr close 1 -R norrisaftcc/tool-teacherbot --comment "$(cat <<'EOF'
  Closing as superseded — every commit on this branch has landed on `main` as
  separate, more granular commits (see `git log origin/main` from 2026-05-12
  onward). Tracking deploy work in a new issue + PR per
  `docs/superpowers/specs/2026-05-16-render-deployment-design.md`.
  EOF
  )"
  ```

- [ ] **Step 4: Confirm it's closed**

  ```bash
  gh pr view 1 -R norrisaftcc/tool-teacherbot --json state,closed
  ```
  Expected: `{"state":"CLOSED","closed":true}`.

---

## Task 6: Open the tracking issue

**Purpose:** Single GitHub artifact where the deploy is tracked from "PR open" through "deployed, verified, command trail captured."

- [ ] **Step 1: Create the issue**

  ```bash
  gh issue create -R norrisaftcc/tool-teacherbot \
    --title "Deploy System 1 to Render (teacherbot, CLI+REST, supersedes 2026-05-13 plan)" \
    --body "$(cat <<'EOF'
  ## Goal

  Deploy `system1-flask-chat/` to Render as service `teacherbot` backed by
  Postgres `teacherbot-db`. Delete the old misconfigured `tool-teacherbot`
  service before creating the new one.

  ## Why a new issue

  The 2026-05-13 plan assumed Render MCP tools that aren't available in the
  agent environment. The 2026-05-16 revision drives the deploy via Render CLI
  (v2.17.0) plus targeted REST calls for the two operations the CLI doesn't
  cover (Postgres creation, service deletion).

  ## Plan

  - Spec: `docs/superpowers/specs/2026-05-16-render-deployment-design.md`
  - Plan: `docs/superpowers/plans/2026-05-16-render-deployment.md`
  - Operator runbook (after deploy): `system1-flask-chat/DEPLOY.md`

  ## Acceptance criteria

  - [ ] Deploy PR merged to `main`
  - [ ] Old `tool-teacherbot` service deleted from the Render workspace
  - [ ] `teacherbot-db` Postgres instance created (status: `available`)
  - [ ] `teacherbot` web service created and deploy reaches `live`
  - [ ] `https://<service-url>/` returns 200/302
  - [ ] `group1`/`capstone2026` login → `/chat` renders, message streams
  - [ ] `/admin?password=<ADMIN_PASSWORD>` lists the conversation
  - [ ] No-op commit to `main` triggers an auto-deploy that reaches `live`
  - [ ] Issue contains a comment trail of every CLI/REST command run

  ## Out of scope

  Filling in group context files; System 2 deployment; replacing query-string
  admin auth; adding CSRF tokens; scaling beyond Render free tier.
  EOF
  )"
  ```

- [ ] **Step 2: Capture the issue number**

  The previous command prints the URL. Extract and save the issue number:
  ```bash
  ISSUE_NUM=$(gh issue list -R norrisaftcc/tool-teacherbot --limit 1 --json number --jq '.[0].number')
  echo "Tracking issue: #$ISSUE_NUM"
  ```
  Save `$ISSUE_NUM` for Task 7.

---

## Task 7: Push the branch and open the deploy PR

**Purpose:** Get the doc/config changes onto GitHub and tied to the tracking issue.

- [ ] **Step 1: Verify clean working tree on the right branch**

  ```bash
  git status
  git branch --show-current
  ```
  Expected: `system1/deploy-render`, working tree clean.

- [ ] **Step 2: Push the branch**

  ```bash
  git push -u origin system1/deploy-render
  ```

- [ ] **Step 3: Open the PR**

  Replace `<ISSUE_NUM>` below with the number from Task 6 Step 2.

  ```bash
  gh pr create -R norrisaftcc/tool-teacherbot \
    --base main \
    --head system1/deploy-render \
    --title "Deploy System 1 to Render: docs, render.yaml, runbook" \
    --body "$(cat <<EOF
  ## Summary

  Repo-side prep for the System 1 Render deploy. No app code changes.

  - New design spec and implementation plan (CLI+REST driven, supersedes 2026-05-13)
  - 2026-05-13 spec/plan marked SUPERSEDED with banners
  - \`render.yaml\` aligned with the new service/DB names (\`teacherbot\` / \`teacherbot-db\`) and validated with \`render blueprints validate\`
  - \`system1-flask-chat/DEPLOY.md\` operator runbook (env vars, redeploy, logs, rollback, suspend/resume)
  - README pointer to the runbook

  ## Test plan

  - [x] \`render blueprints validate render.yaml\` passes
  - [ ] PR merges cleanly to main
  - [ ] After merge, cloud-side provisioning runs per the 2026-05-16 plan (Phase B)

  Closes #${ISSUE_NUM}.
  EOF
  )"
  ```

- [ ] **Step 4: Verify the PR exists and is linked**

  ```bash
  gh pr view --json number,state,headRefName,body
  ```
  Expected: state OPEN, head ref `system1/deploy-render`, body contains `Closes #${ISSUE_NUM}`.

---

## Task 8: Merge the PR

**Purpose:** Get the canonical deploy doc + the corrected `render.yaml` onto `main` before Phase B starts. Future auto-deploys read from `main`.

- [ ] **Step 1: Request user review**

  Tell the user the PR is up and ask them to review and approve. Do NOT auto-merge without their go-ahead. The user owns merge timing.

- [ ] **Step 2: After approval, merge**

  Once the user confirms:
  ```bash
  gh pr merge --squash --delete-branch
  ```
  Expected: PR closed, branch deleted on remote.

- [ ] **Step 3: Sync local main**

  ```bash
  git checkout main
  git pull origin main
  ```
  Expected: local `main` is fast-forwarded to include the squash commit.

---

# Phase B — Cloud provisioning

> Phase B starts only after Phase A merges. Every command in Phase B should be
> recorded as a comment on the tracking issue (`gh issue comment $ISSUE_NUM`)
> so the operator trail is preserved. Show the command and its trimmed output;
> redact `Authorization:` headers and never echo `ANTHROPIC_API_KEY`.

## Task 9: Capture secrets

**Purpose:** Have the three secret env var values ready before creating the service. Without them the service will boot with defaults that don't work.

- [ ] **Step 1: Generate `FLASK_SECRET_KEY`**

  ```bash
  FLASK_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
  echo "FLASK_SECRET_KEY length: ${#FLASK_SECRET_KEY}"
  ```
  Expected: length 64.

- [ ] **Step 2: Confirm `RENDER_API_KEY` is exported**

  ```bash
  test -n "$RENDER_API_KEY" && echo "OK: RENDER_API_KEY is set (length ${#RENDER_API_KEY})" || echo "MISSING"
  ```
  Expected: `OK: RENDER_API_KEY is set (length …)`.

  If `MISSING`: have the user generate one at
  https://dashboard.render.com/u/settings → API Keys → Create. Export with
  `export RENDER_API_KEY=rnd_…`.

- [ ] **Step 3: Confirm `ANTHROPIC_API_KEY` is available**

  Ask the user to paste their key, then capture into a shell variable in the
  same shell (do not write to a file):
  ```bash
  read -s -p "Paste ANTHROPIC_API_KEY (starts with sk-ant-): " ANTHROPIC_API_KEY
  echo
  echo "Key starts with: ${ANTHROPIC_API_KEY:0:8}…"
  ```
  Expected: starts with `sk-ant-`.

- [ ] **Step 4: Pick `ADMIN_PASSWORD`**

  ```bash
  ADMIN_PASSWORD="teacherbot-admin-$(date +%Y%m)"
  echo "ADMIN_PASSWORD=$ADMIN_PASSWORD"
  ```
  This produces e.g. `teacherbot-admin-202605`. Substitute a custom value if the
  user prefers.

- [ ] **Step 5: Sanity-check Render API key**

  ```bash
  curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
    https://api.render.com/v1/owners | jq '.[] | .owner | {id, name}'
  ```
  Expected: at least one owner record. If the response is `{"message":"unauthorized"}` or empty, the key is wrong — fix before continuing.

---

## Task 10: Delete the old `tool-teacherbot` service via REST

**Purpose:** Free the slot so the new service can be created cleanly. The CLI cannot delete services.

- [ ] **Step 1: Re-confirm the service ID**

  ```bash
  render workspace set tea-d81rjp0sfn5c738tl430
  OLD_SRV=$(render services --output json | jq -r '.[] | select(.service.name=="tool-teacherbot") | .service.id')
  echo "Old service ID: $OLD_SRV"
  ```
  Expected: `srv-d81rsrv7f7vs73eeihmg` (or whatever ID the JSON returns). If the variable is empty, the service is already gone — skip to Task 11.

- [ ] **Step 2: Delete via REST**

  ```bash
  curl -s -X DELETE \
    -H "Authorization: Bearer $RENDER_API_KEY" \
    -w "\nHTTP %{http_code}\n" \
    https://api.render.com/v1/services/$OLD_SRV
  ```
  Expected: empty body, `HTTP 204`. If the status is 404 the service was already deleted (treat as success). Any other status (401, 403, 5xx) — stop and surface the response to the user.

- [ ] **Step 3: Verify it's gone**

  ```bash
  render services --output json | jq -r '.[] | .service.name' | sort
  ```
  Expected: the list does not contain `tool-teacherbot`.

- [ ] **Step 4: Comment on tracking issue**

  ```bash
  gh issue comment $ISSUE_NUM -R norrisaftcc/tool-teacherbot \
    --body "Deleted old service \`tool-teacherbot\` ($OLD_SRV) via \`DELETE /v1/services/$OLD_SRV\`. HTTP 204."
  ```

---

## Task 11: Create `teacherbot-db` Postgres via REST

**Purpose:** The web service needs `DATABASE_URL` at creation time. The DB must exist first.

- [ ] **Step 1: Resolve the workspace owner ID**

  The REST endpoint requires an `ownerId`:

  ```bash
  OWNER_ID=$(curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
    https://api.render.com/v1/owners | jq -r '.[0].owner.id')
  echo "Owner ID: $OWNER_ID"
  ```
  Expected: a string starting with `tea-`. Should match `tea-d81rjp0sfn5c738tl430`.

- [ ] **Step 2: Create the DB**

  ```bash
  curl -s -X POST \
    -H "Authorization: Bearer $RENDER_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"name\": \"teacherbot-db\",
      \"ownerId\": \"$OWNER_ID\",
      \"plan\": \"free\",
      \"region\": \"virginia\",
      \"version\": \"16\"
    }" \
    https://api.render.com/v1/postgres | tee /tmp/teacherbot-db.json | jq '{id, name, status, plan, region}'
  ```
  Expected: JSON with `name: "teacherbot-db"`, `status: "creating"` or similar, `plan: "free"`, `region: "virginia"`. Note the `id` (starts with `dpg-`).

  ```bash
  DB_ID=$(jq -r '.id' /tmp/teacherbot-db.json)
  echo "DB ID: $DB_ID"
  ```

  > If the response is an error (e.g. `{"message":"name already exists"}`), the
  > DB was created in a previous attempt; retrieve its ID instead:
  > ```bash
  > DB_ID=$(curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
  >   https://api.render.com/v1/postgres | \
  >   jq -r '.[] | .postgres | select(.name=="teacherbot-db") | .id')
  > echo "DB ID: $DB_ID"
  > ```

- [ ] **Step 3: Poll until status is `available`**

  ```bash
  for i in $(seq 1 30); do
    STATUS=$(curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
      https://api.render.com/v1/postgres/$DB_ID | jq -r '.status')
    echo "[$i] status=$STATUS"
    [ "$STATUS" = "available" ] && break
    sleep 10
  done
  ```
  Expected: within ~2 minutes, `status=available`. If it never becomes available, surface the JSON response to the user and stop.

- [ ] **Step 4: Fetch the connection string**

  ```bash
  DATABASE_URL=$(curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
    https://api.render.com/v1/postgres/$DB_ID/connection-info | \
    jq -r '.externalConnectionString // .internalConnectionString')
  echo "DATABASE_URL: ${DATABASE_URL:0:32}…"
  ```
  Expected: a string starting with `postgresql://`. Length > 50.

  > Use `externalConnectionString` because the web service has not been created
  > yet, so it isn't in the same private network. After the web service is
  > created, Render automatically wires the internal URL into the env var if
  > the YAML uses `fromDatabase`. We're using inline env vars, so we stick
  > with the external URL — `app.py` normalizes the dialect either way.

- [ ] **Step 5: Comment on tracking issue**

  ```bash
  gh issue comment $ISSUE_NUM -R norrisaftcc/tool-teacherbot --body "$(cat <<EOF
  Created \`teacherbot-db\` ($DB_ID).
  - Plan: free, region virginia, version 16
  - Status: available
  - Connection string captured (not pasted here for safety; lives in deploy shell only)
  EOF
  )"
  ```

---

## Task 12: Create the `teacherbot` web service via CLI

**Purpose:** Create the service with all four env vars set at creation time — avoids a separate "set env var" step that would require an unnecessary restart.

- [ ] **Step 1: Create the service**

  ```bash
  render services create \
    --name teacherbot \
    --type web_service \
    --runtime python \
    --repo https://github.com/norrisaftcc/tool-teacherbot \
    --branch main \
    --root-directory system1-flask-chat \
    --build-command "pip install -r requirements.txt" \
    --start-command 'gunicorn "app:create_app()"' \
    --region virginia \
    --plan free \
    --auto-deploy \
    --env-var "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" \
    --env-var "FLASK_SECRET_KEY=$FLASK_SECRET_KEY" \
    --env-var "ADMIN_PASSWORD=$ADMIN_PASSWORD" \
    --env-var "DATABASE_URL=$DATABASE_URL" \
    --output json | tee /tmp/teacherbot-service.json | jq '{id, name, serviceDetails: {url, region, plan}}'
  ```
  Expected: JSON with `name: "teacherbot"`, a service `id` starting with `srv-`, `serviceDetails.url` starting with `https://teacherbot`.

- [ ] **Step 2: Save the service ID and URL**

  ```bash
  SRV_ID=$(jq -r '.id // .service.id' /tmp/teacherbot-service.json)
  SRV_URL=$(jq -r '.serviceDetails.url // .service.serviceDetails.url' /tmp/teacherbot-service.json)
  echo "SRV_ID=$SRV_ID"
  echo "SRV_URL=$SRV_URL"
  ```
  Expected: both non-empty.

- [ ] **Step 3: Comment on tracking issue**

  ```bash
  gh issue comment $ISSUE_NUM -R norrisaftcc/tool-teacherbot --body "$(cat <<EOF
  Created web service \`teacherbot\` ($SRV_ID) at $SRV_URL.
  All four env vars set inline at creation; first build/deploy is underway.
  EOF
  )"
  ```

---

## Task 13: Wait for the initial deploy to reach `live`

**Purpose:** First deploy from a clean service does build + boot + DB connect. Anywhere this fails, we need to read the logs.

- [ ] **Step 1: Poll the deploy list**

  ```bash
  for i in $(seq 1 30); do
    DEP_STATUS=$(render deploys list $SRV_ID --output json | jq -r '.[0].deploy.status')
    DEP_ID=$(render deploys list $SRV_ID --output json | jq -r '.[0].deploy.id')
    echo "[$i] deploy=$DEP_ID status=$DEP_STATUS"
    case "$DEP_STATUS" in
      live)          break ;;
      build_failed|update_failed|canceled|deactivated) echo "DEPLOY FAILED"; break ;;
    esac
    sleep 20
  done
  ```
  Expected: `status=live` within 5 minutes for a free-tier first deploy.

- [ ] **Step 2: If failed, pull the last 200 log lines**

  Only if `DEP_STATUS` is anything other than `live`:
  ```bash
  render logs --resources $SRV_ID --limit 200 --output json | jq -r '.logs[].message' | tail -200
  ```
  Common failures:
  - `psycopg.OperationalError` connecting to DB → check that `DATABASE_URL`
    in env vars matches the connection string for `teacherbot-db`
  - `ModuleNotFoundError` → `requirements.txt` not found; verify
    `--root-directory system1-flask-chat`
  - Gunicorn `Failed to find application object 'create_app()'` → start
    command was misquoted

  Fix the root cause in a follow-up commit on `main` (auto-deploys will pick
  it up) or via `render services update` for non-code issues.

- [ ] **Step 3: Comment on tracking issue with the result**

  ```bash
  gh issue comment $ISSUE_NUM -R norrisaftcc/tool-teacherbot --body "Initial deploy $DEP_ID reached status \`$DEP_STATUS\`."
  ```

---

## Task 14: HTTP smoke tests

**Purpose:** Prove the service is reachable, the login form renders, the auth path round-trips, and the admin endpoint is gated. These tests do not touch Claude — that's the user's job in Task 15.

- [ ] **Step 1: Root page returns 200 (or 302 to /login)**

  ```bash
  curl -sI "$SRV_URL/" | head -1
  ```
  Expected: `HTTP/2 200` or `HTTP/2 302`. If 5xx, the app crashed on boot — check logs.

- [ ] **Step 2: Anonymous /chat redirects to login**

  ```bash
  curl -sI -o /dev/null -w "%{http_code} %{redirect_url}\n" "$SRV_URL/chat"
  ```
  Expected: `302 https://…/login` (path ends in `/login`).

- [ ] **Step 3: Login round-trip**

  ```bash
  curl -s -c /tmp/teacherbot.jar -o /dev/null -w "%{http_code}\n" \
    -X POST -d "group_id=group1&password=capstone2026" "$SRV_URL/login"
  ```
  Expected: `302`. The cookie jar `/tmp/teacherbot.jar` now contains the
  session cookie.

- [ ] **Step 4: Authenticated /chat returns 200**

  ```bash
  curl -s -b /tmp/teacherbot.jar -o /dev/null -w "%{http_code}\n" "$SRV_URL/chat"
  ```
  Expected: `200`.

- [ ] **Step 5: Admin endpoint reachable with correct password**

  ```bash
  curl -s -o /dev/null -w "%{http_code}\n" \
    "$SRV_URL/admin?password=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$ADMIN_PASSWORD")"
  ```
  Expected: `200`.

- [ ] **Step 6: Admin endpoint denies with wrong password**

  ```bash
  curl -s -o /dev/null -w "%{http_code}\n" "$SRV_URL/admin?password=obviously-wrong"
  ```
  Expected: `403`, `401`, or a redirect (anything but `200`). Inspect `routes.py` if it returns 200 — that would indicate auth is broken.

- [ ] **Step 7: Comment on tracking issue with results**

  Build a single comment summarizing each curl's exit status and HTTP code, then post.

---

## Task 15: Hand off to user for browser smoke test

**Purpose:** Verify the Claude integration end-to-end. Streaming SSE responses are easiest to confirm in a browser; curl can verify the endpoint but not the rendered UX.

- [ ] **Step 1: Tail logs in another shell**

  ```bash
  render logs --resources $SRV_ID
  ```
  Leave this running.

- [ ] **Step 2: Tell the user what to do**

  Send a message like:

  > Browser smoke test ready. Please:
  > 1. Open `$SRV_URL` in a browser
  > 2. Log in as `group1` / `capstone2026`
  > 3. Send the message: "Hello, what project is my team working on?"
  > 4. Confirm the response streams in token-by-token and looks coherent
  > 5. Confirm a markdown render of the final response appears
  > 6. Visit `$SRV_URL/admin?password=$ADMIN_PASSWORD` and confirm your conversation is listed
  > 7. Tell me "pass" or report what looked wrong

  Wait for the user's response.

- [ ] **Step 3: If the user reports a problem, diagnose from logs**

  Look at the tailed `render logs` for the test request. Common patterns:
  - `anthropic.APIStatusError: 401` → `ANTHROPIC_API_KEY` is wrong or expired
  - `anthropic.APIStatusError: 404 model not found` → model id in
    `claude_handler.py` isn't valid; check what's pinned
  - 500s with `IntegrityError` → DB schema didn't initialize (rare; `db.create_all()` runs on startup)

- [ ] **Step 4: Comment on tracking issue with user's verdict**

  ```bash
  gh issue comment $ISSUE_NUM -R norrisaftcc/tool-teacherbot --body "User browser smoke test: <pass/fail with notes>."
  ```

---

## Task 16: Prove auto-deploy with a no-op commit

**Purpose:** Confirm that pushing to `main` triggers a fresh deploy without manual intervention. Last verification before declaring the deploy done.

- [ ] **Step 1: Make a trivial commit on main**

  ```bash
  git checkout main
  git pull origin main
  printf "\n<!-- deploy verified %s -->\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> system1-flask-chat/DEPLOY.md
  git add system1-flask-chat/DEPLOY.md
  git commit -m "$(cat <<'EOF'
  chore: verify auto-deploy on push to main

  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  EOF
  )"
  git push origin main
  ```

- [ ] **Step 2: Watch for a new deploy to start within ~30 seconds**

  ```bash
  PRE=$(render deploys list $SRV_ID --output json | jq -r '.[0].deploy.id')
  for i in $(seq 1 6); do
    NOW=$(render deploys list $SRV_ID --output json | jq -r '.[0].deploy.id')
    echo "[$i] head deploy id: $NOW (was $PRE)"
    [ "$NOW" != "$PRE" ] && echo "AUTO-DEPLOY STARTED: $NOW" && break
    sleep 10
  done
  ```
  Expected: within a minute, a new deploy ID appears.

- [ ] **Step 3: Wait for the new deploy to reach `live`**

  Reuse the polling loop from Task 13 Step 1 with `NOW` as the expected deploy
  ID. Expected: `status=live` within 3 minutes.

- [ ] **Step 4: Re-check the live URL**

  ```bash
  curl -sI "$SRV_URL/" | head -1
  ```
  Expected: 200 or 302 (the site is still up after the deploy).

---

## Task 17: Final issue comment and close

**Purpose:** Land the operator handoff. After this, anyone reading the issue knows the service is live, where the docs are, and what to do next.

- [ ] **Step 1: Compose and post the closing comment**

  ```bash
  gh issue comment $ISSUE_NUM -R norrisaftcc/tool-teacherbot --body "$(cat <<EOF
  ## Deploy complete

  - Service: \`teacherbot\` ($SRV_ID)
  - Database: \`teacherbot-db\` ($DB_ID)
  - URL: $SRV_URL
  - Admin URL: $SRV_URL/admin?password=\<ADMIN_PASSWORD\>

  ### Acceptance criteria

  - [x] Deploy PR merged to main (see PR linked above)
  - [x] Old \`tool-teacherbot\` deleted
  - [x] \`teacherbot-db\` Postgres available
  - [x] \`teacherbot\` web service reached \`live\`
  - [x] HTTP smoke tests pass
  - [x] Browser smoke test pass (user-confirmed)
  - [x] Auto-deploy verified with a no-op commit
  - [x] Command trail captured in this issue

  ### Next steps for the instructor

  1. Fill in the placeholder context files at
     \`system1-flask-chat/context/group*_context.md\`, commit, push — auto-deploy
     will pick them up.
  2. Rotate \`ADMIN_PASSWORD\` before any classroom use.
  3. File a follow-up issue to replace the query-string admin auth with a
     proper login form before public exposure.

  Operator runbook: \`system1-flask-chat/DEPLOY.md\`.
  EOF
  )"
  ```

- [ ] **Step 2: Close the issue**

  ```bash
  gh issue close $ISSUE_NUM -R norrisaftcc/tool-teacherbot
  ```

- [ ] **Step 3: Confirm closed**

  ```bash
  gh issue view $ISSUE_NUM -R norrisaftcc/tool-teacherbot --json state
  ```
  Expected: `{"state":"CLOSED"}`.

---

## Task 18: Clean up local secrets

**Purpose:** The shell variables holding `ANTHROPIC_API_KEY`, `ADMIN_PASSWORD`, and `DATABASE_URL` should not linger.

- [ ] **Step 1: Unset all secret shell variables**

  ```bash
  unset ANTHROPIC_API_KEY FLASK_SECRET_KEY ADMIN_PASSWORD DATABASE_URL
  # RENDER_API_KEY stays exported in the user's shell only if they want it for
  # future operations; otherwise: unset RENDER_API_KEY
  rm -f /tmp/teacherbot.jar /tmp/teacherbot-db.json /tmp/teacherbot-service.json
  ```

- [ ] **Step 2: Sanity check**

  ```bash
  set | grep -E '^(ANTHROPIC_API_KEY|FLASK_SECRET_KEY|ADMIN_PASSWORD|DATABASE_URL)=' || echo "OK: all cleared"
  ```
  Expected: `OK: all cleared`.

---

## Done.

The deploy is live and the issue is closed. Future operations use
`system1-flask-chat/DEPLOY.md`. Future agents reading this plan can re-execute
it idempotently — the "if already exists, look it up instead" branches in
Task 10 and Task 11 are deliberate.
