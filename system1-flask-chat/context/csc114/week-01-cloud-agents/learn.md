# Learn — What is an agent, really?

**Slot:** Learn (low-stakes, no submission)
**Time:** ~25 minutes
**Goal:** Walk into [practice.md](practice.md) knowing what you're about to build and why.

---

## Three things, ranked

Imagine three AI systems:

1. **A customer service chatbot** that answers FAQ questions from a script.
2. **A personal assistant** that can check your calendar, draft emails, and book a restaurant when you ask.
3. **A research tool** you give a topic to, and it autonomously searches the web, reads papers, takes notes, decides what else to search, and delivers a report — all without you touching anything until the end.

They're all "AI." What's different?

| | Chatbot | Assistant | Agent |
|---|---|---|---|
| Uses tools? | No | Yes, when asked | Yes, autonomously |
| Loops? | Single turn | Multi-turn, you drive | Multi-turn, *it* drives |
| Decides what to do next? | Never | Sometimes | Always |
| Runs unsupervised? | N/A | Briefly | For extended periods |

**The line that matters:** an agent is an AI that uses tools in a *loop*, deciding what to do next, with minimal human intervention.

## Why this is a hard system to build from scratch

If you had to build the research-tool agent yourself, you'd need:

- A loop ("keep going until you're done").
- A sandbox where the agent can run code without breaking your laptop.
- A tool dispatcher (the agent says "I want to search for X" — something has to actually run the search).
- A way to give the agent files, credentials, environment.
- A way to watch what it's doing and stop it if it goes sideways.

That whole thing is called the **harness**. Building one is real work — months of it. Claude Managed Agents is Anthropic's hosted harness. You don't build the loop; you bring the brain (the system prompt) and tell the harness what tools the agent is allowed to touch.

## The five things in the Console

When you log in to `platform.claude.com` and look at the left sidebar, you'll see five things. Here they are with the "office" analogy:

- **Agent** — a job description. What does this employee know? What tools are they allowed to use? What reference materials (Skills) have they been trained on? Editing the agent creates a new version, like updating a job description.
- **Environment** — the office itself. What software is installed? What's the network policy (can this office make outside calls?)? Shared across multiple sessions.
- **Session** — a workday. One agent, one environment, one task. When the session ends, the desk is cleared. Next session starts fresh.
- **Credential Vault** — the key cabinet. API tokens and OAuth credentials live here. The agent never sees the raw key; the building's security system handles it.
- **Skill** — a reference manual on the shelf. A folder with a `SKILL.md` and supporting scripts that teach the agent a specific capability ("how to create a PowerPoint file"). We won't write Skills this week.

You don't have to memorize this. You'll touch all five over the course of the term. Right now, just **know what they are when you see them in the sidebar**.

## What you're going to build this week

Two things, in order:

1. **A trivially simple "Campus Info Bot"** — your warm-up. Five facts about a department, a fallback when it doesn't know. This exists so you fight the *Console UI*, not the *agent design*, on your first try.
2. **A domain agent of your own choice** — a real thing. Subnetting calculator. Recipe assistant. Help-desk triage bot. Academic advising bot. Whatever subject area you can describe in three "must answer" questions and one "must refuse" question.

The warm-up is in [practice.md](practice.md). The real build is in [apply.md](apply.md). You'll do the warm-up Monday/Tuesday and the real build Wednesday/Thursday.

## One concept to land before you go further

**The system prompt is the product.**

The Console gives you an interface. The model gives you general intelligence. *Your work* is the system prompt — the constraints, the role, the domain facts, the output format. A vague prompt produces a vague agent. A precise prompt produces a precise agent. This is the part of agent development that takes *time and judgment*, and it's the part nobody else can do for you.

You will rewrite your system prompt a lot this week. That's the job, not a sign you're doing it wrong.

## Where to go next

→ [practice.md](practice.md) — Console warm-up. Get the mechanics in your fingers before you try anything ambitious.
