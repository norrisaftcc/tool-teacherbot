> **HISTORICAL — do not act on this file.** It describes a project shape
> (five capstone groups, two parallel systems) that the code stopped
> matching in July 2026. Kept as a paper trail. For what is actually
> true, read `docs/adr/`, `docs/registry/KEEP.md`, and
> `system1-flask-chat/DEPLOY.md`.

# HANDOFF TO IMPLEMENTERS

**Status**: Ready for parallel development by two Claude Code instances

**Repository**: `/home/claude/ta-systems-alpha/`

---

## For the Human: What You Need

Before launching the Claude Code instances:

1. **Anthropic API Keys**:
   - 1 key for System 1 (Flask app - will go in Render dashboard)
   - 5 keys for System 2 (one per group - will be distributed)
   - Get these from: https://console.anthropic.com/

2. **Render Account**:
   - Sign up at https://render.com (free tier works for alpha)
   - Will deploy System 1 Flask app here

3. **Group Information** (optional - can be placeholder for now):
   - Group names (group1, group2, etc.)
   - Project names (DataMan, FinAid Tracker, etc.)
   - Tech stacks (Flask/React, Flask/Vue, etc.)
   - Current sprint focus

---

## Repository Structure (Ready to Go)

```
ta-systems-alpha/
├── README.md                           # Quick start guide
├── TA_SYSTEMS_PARALLEL_PLAN.md         # Complete technical spec
├── HANDOFF.md                          # This file
│
├── system1-flask-chat/                 # INSTANCE A WORKS HERE
│   ├── CLAUDE.md                       # Instance A's guide
│   ├── templates/                      # (empty, A will create)
│   ├── static/css/                     # (empty, A will create)
│   └── context/                        # (empty, A will create)
│
├── system2-code-distribution/          # INSTANCE B WORKS HERE
│   ├── CLAUDE.md                       # Instance B's guide
│   ├── config_templates/               # (empty, B will create)
│   └── documentation/                  # (empty, B will create)
│
├── shared/                             # BOTH COORDINATE HERE
│   └── (will be created by instances)
│
└── docs/                               # (will be created by instances)
```

---

## Launch Sequence

### Step 1: Verify Repository
```bash
cd /home/claude/ta-systems-alpha
git status
# Should show: On branch master, clean working directory
```

### Step 2: Launch Instance A (System 1)
```bash
# In Terminal 1
cd system1-flask-chat
claude-code
```

**First Prompt**:
```
I'm working on System 1 (Flask chat interface for AlgoCratic TA system).

Please read CLAUDE.md in this directory for complete context, then:
1. Confirm you understand the project
2. Tell me what file we should create first
3. Wait for my approval before proceeding

Timeline: We have 20 hours to reach deployment-ready state.
Current hour: 0 (just starting)
```

### Step 3: Launch Instance B (System 2)
```bash
# In Terminal 2
cd system2-code-distribution
claude-code
```

**First Prompt**:
```
I'm working on System 2 (Claude Code distribution framework for AlgoCratic TA system).

Please read CLAUDE.md in this directory for complete context, then:
1. Confirm you understand the project
2. Tell me what file we should create first
3. Wait for my approval before proceeding

Timeline: We have 20 hours to reach deployment-ready state.
Current hour: 0 (just starting)

Note: Instance A is working in parallel on System 1. We coordinate on shared/ files.
```

---

## What Each Instance Will Build

### Instance A (System 1) - Hours 0-20
**Hours 0-4**: Flask skeleton + Claude API integration
- `app.py` with basic routes
- `claude_handler.py` for API calls
- Test: Send message, get Claude response

**Hours 4-8**: Database + persistence
- `models.py` with Group, Conversation, Message
- Database migrations
- Conversation logging working

**Hours 8-12**: Context + Admin
- `context/` with group context files
- Admin dashboard showing logs and token usage
- Context injection tested

**Hours 12-16**: Deployment
- `render.yaml` configuration
- PostgreSQL migration
- Deploy to Render, test live

**Hours 16-20**: Polish
- Error handling
- Security review
- Documentation

### Instance B (System 2) - Hours 0-20
**Hours 0-4**: Setup automation
- `setup.py` that generates group configs
- Test with 2 sample groups

**Hours 4-8**: Templates
- `config_templates/CLAUDE_template.md`
- Template rendering with group data
- Test Claude Code reads and follows

**Hours 8-12**: Documentation
- `documentation/instructor_guide.md`
- `documentation/student_guide.md`
- Complete with examples

**Hours 12-16**: Spend tracking
- `check_budget.py` script
- Token usage tracking
- Test budget calculations

**Hours 16-20**: Integration
- Optional webhook to System 1
- End-to-end testing
- Final docs review

---

## Coordination Points

### When Instances Need to Talk

**Scenario 1**: Instance A creates database schema
- A creates `shared/database_schema.sql`
- A commits: `git commit -m "System 1: Initial database schema"`
- A creates PR: `git push origin system1/database-schema`
- B reviews PR, adds `api_usage` table if needed
- A merges after B approves

**Scenario 2**: Instance B needs context format
- B reads `shared/group_context_template.md` (created by A)
- B uses same format in CLAUDE.md templates
- No conflict - B just reads, doesn't modify

**Scenario 3**: Both want to modify shared file
- First instance creates PR
- Second instance waits for merge
- Second instance pulls and rebases
- Second instance makes their changes

---

## Success Criteria (Alpha)

After 20-24 hours, you should have:

**System 1**:
- [ ] Deployed on Render at `https://your-app.onrender.com`
- [ ] Can log in as group1, group2, etc.
- [ ] Claude responds with context-aware answers
- [ ] Conversations logged to database
- [ ] Admin dashboard shows usage

**System 2**:
- [ ] `setup.py` generates valid group configs
- [ ] 5 group folders created and customized
- [ ] Documentation complete (instructor + student)
- [ ] Ready to distribute to groups

**Integration**:
- [ ] Both systems use same context format
- [ ] Token tracking works in both
- [ ] No file conflicts or merge issues
- [ ] End-to-end tested

---

## Emergency Contacts

**If an instance gets stuck**:
1. Read the parallel plan: `TA_SYSTEMS_PARALLEL_PLAN.md`
2. Check reference repos:
   - `/home/claude/algorithm-shodann/` (pedagogical patterns)
   - `/home/claude/tool-algoflow-py/` (session management)
3. Create GitHub issue with `blocker` label
4. Other instance can help unblock

**If instances conflict**:
1. Use GitHub PRs for coordination
2. Comment on PRs with questions
3. Don't force-push or overwrite work

**If timeline slips**:
- Focus on MVP only (no optional features)
- System 1 is higher priority (students need it now)
- System 2 can be finished slightly after if needed

---

## Post-Alpha Plans

After alpha deployment, consider:
- Growth velocity tracking (connect to GitHub commits)
- Multiple clearance level support
- Conversation search in admin dashboard
- Automated budget warnings
- Cross-system SSO

But for now: **Ship the alpha. Students are waiting.**

---

## Final Checklist Before Launch

- [ ] Anthropic API keys obtained
- [ ] Render account created
- [ ] Group information gathered (or placeholders ready)
- [ ] Repository structure verified
- [ ] Two terminals ready for Claude Code
- [ ] Coffee/energy drink acquired ☕

---

**Ready to ship. frotz → plugh. The Algorithm awaits deployment.**
