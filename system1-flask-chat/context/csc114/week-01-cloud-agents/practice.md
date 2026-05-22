# Practice — Console warm-up: Campus Info Bot

**Slot:** Practice (retry-OK, no grade penalty for failed tries)
**Time:** ~45 minutes
**Goal:** Build a deliberately trivial agent so you fight the Console UI, not the agent design, on your first attempt.

---

## What we're doing

You're going to make an agent that knows five facts about a department on your campus (or a fictional one) and can say "I don't know" when asked something else. That's it. The point is **mechanical fluency** — by the end you should be able to click through *Agents → New Agent → name → model → system prompt → save → create session → test* without thinking about which menu is which.

If your bot is boring after this lab, you did it right.

## Steps

### 1. Log in

- Go to [`platform.claude.com`](https://platform.claude.com).
- Sign in with the account you set up in Module 0.
- In the workspace switcher (top-left), make sure you're in **`csc114-summer-2026`**, not your personal workspace.

If you can't get to the class workspace, stop and re-read `planning/legacy_csc113/m00-setup-package.md`. Don't try to do this lab from your personal workspace — you'll hit billing limits later.

### 2. Create your agent

- Left sidebar: **Agents → New Agent**.
- Name: `{your-initials}-campus-bot` (example: `jd-campus-bot`).
- Model: select **`claude-sonnet-4-6`** from the dropdown. *Don't change this.* We always start at Sonnet; you earn the right to upgrade to Opus only after you've proven Sonnet can't do the job.
- System prompt — paste this and fill in the bracketed bits:

```
You are a helpful information assistant for the [Department Name] department
at [College Name]. The current date is [today's date].

Your knowledge:
- The department office is located in [Building], Room [Number].
- Office hours are [days] from [time] to [time].
- The department chair is [Name]. Contact: [email or phone].
- [Add two more specific facts about your department.]

Rules:
- Only answer questions using the information above.
- If someone asks something you don't know, say: "I don't have that
  information. Please contact the department office at [phone/email]."
- Never make up information. Never guess.
- Be friendly and professional.
```

- Tools: leave the default `agent_toolset_20260401` on. We'll learn to scope tools down in [apply.md](apply.md). For now, leaving it broad is fine.
- Click **Save**.

You should see a confirmation that version 1 of your agent exists.

### 3. Run a test session

- Left sidebar: **Sessions → Create Session**.
- Pick your agent and the **`class-shared`** environment (your instructor pre-created this).
- Send these three messages, one at a time, and watch the response after each:

| Test | What to send | What you're checking |
|---|---|---|
| Happy path | A question your bot **can** answer — pick one from your 5 facts (e.g., "Where is the office?") | Does it give the correct information? |
| Fallback | A question it **cannot** answer (e.g., "What's the GPA requirement for the program?") | Does it say "I don't know," or does it make something up? |
| Trick question | Something plausible but not in your prompt (e.g., "Is Dr. Smith teaching next semester?") | Does it hallucinate a plausible-sounding answer? |

### 4. Read the Debug view

- After your test, switch to the **Debug** tab (next to Transcript).
- Find the token count for one of your conversations.
- Write down or screenshot: input tokens, output tokens, total.

We're not doing cost calculation this week. You're just *seeing* that the tokens exist and where they live.

### 5. Save what you did to GitHub

Make a folder in your course repo called `week-01/` and add two files:

- `system-prompt-v1.md` — the system prompt text you used (the filled-in version, not the template).
- `testing-log.md` — your three test results, in this format:

```markdown
# Testing Log — Week 1

## Campus Info Bot

| Test # | Input | Expected behavior | Actual behavior | Pass/Fail | Notes |
|---|---|---|---|---|---|
| 1 | "Where is the office?" | Gives correct location | [what happened] | [P/F] | |
| 2 | "What's the GPA requirement?" | Says "I don't know" | [what happened] | [P/F] | |
| 3 | "Is Dr. Smith teaching next semester?" | Refuses to guess | [what happened] | [P/F] | |

**Token count (Test 1):** Input: ___ | Output: ___ | Total: ___
```

How you put those files in the repo is up to you this week — GitHub Desktop, the web "add file" button, or `git` from the terminal. Sacred Flow (branches, PRs) starts Week 2.

## Before you leave Practice

- [ ] Your `{your-initials}-campus-bot` agent exists in the Console.
- [ ] You ran three test conversations and *observed how the agent behaved on each*.
- [ ] `week-01/system-prompt-v1.md` and `week-01/testing-log.md` are in your repo.

## Common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| "I can't find where to create an agent" | UI confusion | Left sidebar → Agents → New Agent. |
| Agent makes up answers to test 2 or 3 | System prompt too vague | Strengthen the "never make up information" rule, save a v2, re-test. |
| Session won't start | No environment selected | Pick the `class-shared` environment when creating the session. |
| "It's really slow" | Opus selected by mistake | Check the model dropdown. Should be `claude-sonnet-4-6`. |

## Where to go next

→ [apply.md](apply.md) — Build a domain agent v1. This is the real work for the week.
