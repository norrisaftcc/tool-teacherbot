# Week 1 — Cloud Agents (Module 0)

**Pilot week:** 1 of 8 (CSC-114 Summer 2026)
**Theme:** Before we touch the textbook, you build something. By Friday you have a working AI agent of your own design in the Claude Console.
**Manning chapter(s):** *None — pre-textbook.* Textbook work begins Week 2.

---

## Why this is Week 1, not later

Two reasons. First, you learn faster when you've already built something — Week 2 (Keras hello-world) lands differently if you've spent a week thinking about what an AI system actually *is*. Second, some of you will keep iterating on your agent the whole term as your real project. That's allowed. The textbook track and the agent track both count, as long as you build something real.

This week is also where the class gets its **GitHub home base** set up. You need an account, you need to be in the course org, and you need to have committed at least one file. We'll keep Sacred Flow (issue → branch → PR → merge) for Week 2 onward — this week you can submit by dragging files into the repo if that's where you are.

## Learning outcomes

By Friday, you can:

1. **Explain** the chatbot → assistant → agent spectrum and where Claude Managed Agents sits on it.
2. **Create** a Claude Managed Agent in the Console, including model selection and system prompt.
3. **Design** a domain-specific system prompt using the five-section template.
4. **Test** an agent using the one-change-rule and document what happened.
5. **Decide intentionally** which tools your agent gets and write down why.

## What you do this week

Read in this order. Each file is one slot of Learn → Practice → Apply → Assess.

1. **[learn.md](learn.md)** — *What is an agent, really?* Read first. Concepts only, no Console yet.
2. **[practice.md](practice.md)** — *Console warm-up: Campus Info Bot.* Retry-OK. Get the mechanics in your fingers.
3. **[apply.md](apply.md)** — *Build your domain agent v1.* This is the real work. The five-section prompt, the one-change-rule, the tool rationale.
4. **[assess.md](assess.md)** — *What you submit.* Screenshot + one paragraph. Both tracks submit the same way this week.

If you finish [apply.md](apply.md) early and want to push further, the original module went deeper into file mounting, MCP servers, security testing, cost calculation, and peer review — the source is at `planning/legacy_csc113/CSC-114_Module_Cloud_Agents_Student_Lab_Packet.md`, Meetings 3 and 4. That's available as a self-directed extension; it's not required for the pilot.

## Two-track expectations this week

Week 1 is **universal low-stakes** — both tracks submit identically.

| Track | What you submit | How |
|-------|-----------------|-----|
| Code Builders | Screenshot of your agent answering correctly + 1-paragraph reflection. | Add files to your repo. GitHub Desktop, the GitHub web UI, or `git` — your choice. No PR required this week. |
| Prompt Masters | Same. | Same. |

Sacred Flow (issues, branches, PRs, merges, retrospectives) starts Week 2 for the Code Builders track. This week your only GitHub job is *get into the course org and put a file in your repo.*

## Before you start

- [ ] Anthropic Console account (created during setup, see `planning/legacy_csc113/m00-setup-package.md`).
- [ ] Membership in the class workspace (`csc114-summer-2026`).
- [ ] GitHub account, accepted invite to the course org.
- [ ] Today's date, written somewhere you can paste it into a system prompt.

If any of those aren't true, fix that first. The setup packet (`planning/legacy_csc113/m00-setup-package.md`) is the source of truth for setup.
