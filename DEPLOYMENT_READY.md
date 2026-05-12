# TA SYSTEMS ALPHA: READY TO DEPLOY

**Repository**: `/home/claude/ta-systems-alpha/`
**Status**: ✅ Ready for handoff to two Claude Code instances
**Commit**: `23fef6e` - "Initial commit: TA Systems Alpha"

---

## What You're Handing Off

A complete, deployment-ready repository for building:
- **System 1**: Flask web chat (Claude API, student auth, conversation logging)
- **System 2**: Claude Code CLI distribution (per-group API keys, pedagogical guardrails)

Both systems designed for **parallel development** by two Claude Code instances working simultaneously.

---

## Repository Contents

```
ta-systems-alpha/
├── README.md                    # Quick start guide
├── HANDOFF.md                   # Launch instructions for instances ⭐
├── TA_SYSTEMS_PARALLEL_PLAN.md  # Complete technical spec
│
├── system1-flask-chat/
│   └── CLAUDE.md                # Instance A's complete guide
│
└── system2-code-distribution/
    └── CLAUDE.md                # Instance B's complete guide
```

---

## Launch Sequence (Copy-Paste Ready)

### Terminal 1: Instance A (System 1)
```bash
cd /home/claude/ta-systems-alpha/system1-flask-chat
claude-code
```

**Paste this as first prompt**:
```
I'm working on System 1 (Flask chat interface for AlgoCratic TA system).

Please read CLAUDE.md in this directory for complete context, then:
1. Confirm you understand the project
2. Tell me what file we should create first
3. Wait for my approval before proceeding

Timeline: We have 20 hours to reach deployment-ready state.
Current hour: 0 (just starting)
```

### Terminal 2: Instance B (System 2)
```bash
cd /home/claude/ta-systems-alpha/system2-code-distribution
claude-code
```

**Paste this as first prompt**:
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

## What You Need Before Launch

### Required
1. **Anthropic API Keys** (get from https://console.anthropic.com/):
   - 1 key for System 1 (Flask app)
   - 5 keys for System 2 (one per group)

2. **Render Account** (https://render.com - free tier OK):
   - For deploying System 1 Flask app

### Optional (Can Use Placeholders)
3. **Group Details**:
   - Group names (group1-5 is fine)
   - Project names (placeholders OK for alpha)
   - Tech stacks (can fill in later)

---

## Timeline (Parallel Execution)

```
Hour 0: Launch both instances
  ├─ Instance A: Flask skeleton + Claude API
  └─ Instance B: Setup script skeleton

Hour 4: Core features working
  ├─ Instance A: Database + conversation logging
  └─ Instance B: Config generation working

Hour 8: Integration begins
  ├─ Instance A: Admin dashboard + context loading
  └─ Instance B: CLAUDE.md templates + documentation

Hour 12: Deployment prep
  ├─ Instance A: Render configuration
  └─ Instance B: Spend tracking + budget scripts

Hour 16: Polish & test
  ├─ Instance A: Security + error handling
  └─ Instance B: End-to-end testing

Hour 20: Alpha ready
  ├─ System 1: Deployed on Render
  └─ System 2: Ready to distribute to groups
```

---

## Coordination Between Instances

The instances will coordinate via:
- **Git branches**: `system1/feature` and `system2/feature`
- **Pull requests**: For changes to `shared/` directory
- **Comments**: On PRs for questions/approvals

You don't need to manage this - they'll handle it themselves using the protocol in HANDOFF.md.

---

## Success Criteria (24 Hours)

### System 1 (Flask Chat)
- [ ] Deployed at https://your-app.onrender.com
- [ ] Group login working (group1, group2, etc.)
- [ ] Claude responds with project context
- [ ] Conversations logged to PostgreSQL
- [ ] Admin dashboard shows token usage

### System 2 (Distribution)
- [ ] `python setup.py --groups 5` works
- [ ] Generates 5 valid group configurations
- [ ] CLAUDE.md templates customized
- [ ] Instructor + student guides complete
- [ ] Ready to distribute to teams

### Integration
- [ ] Both use same context format
- [ ] Token tracking accurate
- [ ] No merge conflicts
- [ ] End-to-end tested

---

## If Something Goes Wrong

**Instance gets stuck**:
- Read `HANDOFF.md` section "Emergency Contacts"
- Check reference repos: `algorithm-shodann/`, `tool-algoflow-py/`
- Create GitHub issue with `blocker` label

**Timeline slips**:
- Focus on MVP only (no optional features)
- Prioritize System 1 (students need it ASAP)
- System 2 can finish slightly after if needed

**Instances conflict**:
- Use PRs for coordination (built into plan)
- First instance creates PR, second reviews
- No force-pushing

---

## What Happens Next

1. **You launch the instances** (5 minutes)
2. **Instances work in parallel** (20 hours)
3. **You monitor progress** (check commits, ask questions)
4. **Alpha deployment** (Hour 20-24)
5. **Students start using it** (immediately after)

---

## Files to Review (Optional)

Before launching, you might want to skim:
- `HANDOFF.md` - What the instances will read first
- `system1-flask-chat/CLAUDE.md` - Instance A's full guide
- `system2-code-distribution/CLAUDE.md` - Instance B's full guide
- `TA_SYSTEMS_PARALLEL_PLAN.md` - Complete technical spec

But these are comprehensive - the instances have everything they need.

---

## Post-Alpha Iterations

After initial deployment works:
- Add growth velocity tracking (dy/dx like SHODANN)
- Multiple clearance level support
- Conversation search in admin
- Automated budget warnings
- Cross-system single sign-on

But first: **Ship the alpha. Iterate from reality.**

---

## Your Role During Development

**Minimal supervision needed**. The instances have:
- ✅ Complete technical specifications
- ✅ Phase-by-phase timelines
- ✅ Coordination protocols
- ✅ Error recovery strategies
- ✅ Success criteria

You just need to:
1. Launch them (paste the prompts)
2. Answer questions if they ask
3. Provide API keys when System 1 deploys
4. Test the result at Hour 20

---

## Final Thoughts

This is **educational infrastructure that teaches growth** - inspired by SHODANN's velocity philosophy, wrapped in AlgoCratic's satirical frame, built with real competence at the core.

The metaphor worked. The resistance provided inspiration. The Algorithm approved the architecture.

**Time to deploy.**

frotz → plugh → ship

---

## Launch Command (When Ready)

```bash
# Terminal 1
cd /home/claude/ta-systems-alpha/system1-flask-chat && claude-code

# Terminal 2  
cd /home/claude/ta-systems-alpha/system2-code-distribution && claude-code
```

**Then paste the prompts from "Launch Sequence" section above.**

✅ Repository ready at: `/home/claude/ta-systems-alpha/`
✅ All documentation complete
✅ Instances can work independently
✅ Coordination protocol established
✅ Success criteria defined

**The Algorithm awaits your command to begin.**
