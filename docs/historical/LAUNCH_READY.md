> **HISTORICAL — do not act on this file.** It describes a project shape
> (five capstone groups, two parallel systems) that the code stopped
> matching in July 2026. Kept as a paper trail. For what is actually
> true, read `docs/adr/`, `docs/registry/KEEP.md`, and
> `system1-flask-chat/DEPLOY.md`.

# 🚀 LAUNCH READY - Real Projects Loaded

**Repository**: `/home/claude/ta-systems-alpha/`  
**Commit**: `81c1099` - "Add real project details"  
**Status**: ✅ **GO FOR LAUNCH**

---

## Real Project Details Added

### 5 Groups Ready to Deploy:
```
Group 0: O.BAG          (login: group0 / obag2026)
Group 1: Steered        (login: group1 / steered2026)
Group 2: BioSync        (login: group2 / biosync2026)
Group 3: StudyStream    (login: group3 / studystream2026)
Group 4: DataMon        (login: group4 / datamon2026)
```

### Context Files:
- ✅ `shared/group_context_template.md` - Template with all 5 projects
- ✅ `shared/group_credentials.md` - Authentication setup for System 1
- ✅ DataMon has partial real context (math platform, Flask/React, auth sprint)
- ✅ Other groups have structure ready for instances to populate

---

## Launch Commands (Copy-Paste Ready)

### Terminal 1: System 1 (Flask Chat)
```bash
cd /home/claude/ta-systems-alpha/system1-flask-chat
claude-code
```

**First Prompt**:
```
I'm working on System 1 (Flask chat interface for AlgoCratic TA system).

Context: We have 5 real capstone groups ready to deploy:
- Group 0: O.BAG
- Group 1: Steered  
- Group 2: BioSync
- Group 3: StudyStream
- Group 4: DataMon

Please read CLAUDE.md in this directory, then:
1. Confirm you understand the project and the 5 groups
2. Check shared/group_context_template.md and shared/group_credentials.md
3. Tell me what file we should create first
4. Wait for my approval before proceeding

Timeline: 20 hours to deployment-ready state. Current hour: 0.
```

### Terminal 2: System 2 (Claude Code Distribution)
```bash
cd /home/claude/ta-systems-alpha/system2-code-distribution
claude-code
```

**First Prompt**:
```
I'm working on System 2 (Claude Code distribution framework).

Context: We have 5 real capstone groups ready:
- Group 0: O.BAG
- Group 1: Steered
- Group 2: BioSync  
- Group 3: StudyStream
- Group 4: DataMon

Please read CLAUDE.md in this directory, then:
1. Confirm you understand the project and the 5 groups
2. Check shared/group_context_template.md for the format
3. Tell me what file we should create first
4. Wait for my approval before proceeding

Timeline: 20 hours to deployment-ready state. Current hour: 0.
Note: Instance A is working in parallel on System 1.
```

---

## What Instances Will Find

### In `shared/` Directory:
1. **group_context_template.md**
   - All 5 project names
   - Template structure for context
   - DataMon has some real details (auth sprint, tech stack)

2. **group_credentials.md**
   - Login credentials for each group
   - Group-to-project mapping
   - Session structure guidance

### Instances Will:
- **Instance A**: Create 5 context files in `context/` using the template
- **Instance B**: Generate 5 group configs using the same project names
- **Both**: Use identical project names and structure

---

## Your Checklist

Before launching:
- ✅ 5 groups identified (O.BAG, Steered, BioSync, StudyStream, DataMon)
- ✅ API keys ready (1 for System 1, 5 for System 2)
- ⏳ Render account (set up when System 1 deploys)
- ✅ Context template created
- ✅ Group credentials defined

After launching:
- Monitor commits (both instances working in parallel)
- Provide API keys when System 1 reaches deployment (Hour ~12-16)
- Test login for each group (Hour ~20)
- Distribute System 2 configs to groups (Hour ~20-24)

---

## Expected Timeline

```
Hour 0:  Launch both instances
Hour 2:  Basic structure in place (Flask skeleton, setup.py skeleton)
Hour 4:  Core features working (API calls, config generation)
Hour 8:  Context loading working, templates rendered
Hour 12: System 1 ready for Render deployment
Hour 16: System 1 deployed, System 2 docs complete
Hour 20: Alpha testing (you can log in as each group)
Hour 24: Production ready, distribute to students
```

---

## Success Looks Like

**System 1** (Hour 20):
```bash
# You can test:
curl https://your-app.onrender.com/
# → Login page

# Login as group0 with password "obag2026"
# → Chat interface loads
# → Send message about O.BAG project
# → Claude responds with O.BAG context awareness
```

**System 2** (Hour 20):
```bash
# Instructor has:
ls
# → group_0/ group_1/ group_2/ group_3/ group_4/

# Each folder contains:
# - .anthropic-key (their API key)
# - CLAUDE.md (customized with project details)
# - spend_cap.json (100k token budget)
# - README.md (setup instructions)

# Ready to email/distribute to each group
```

---

## If You Need to Pause

Repository is version controlled. You can:
```bash
cd /home/claude/ta-systems-alpha
git status  # See current state
git log     # See commit history
```

Instances commit frequently. You can pause at any hour and resume later.

---

## Post-Alpha Improvements

After initial deployment works, you can add:
- More detailed context for O.BAG, Steered, BioSync, StudyStream
- Student names and roles per group
- Sprint-specific guidance
- Known issues from their repos
- Integration with GitHub commits
- Growth velocity tracking

But first: **Ship with what we have. Iterate from reality.**

---

## Launch Authority: GRANTED ✅

All systems nominal. Instances briefed. Context loaded. Projects identified.

**The Algorithm awaits your command.**

```bash
# Terminal 1 & 2: Ready for launch
# Paste commands from "Launch Commands" section above
```

frotz → plugh → **SHIP IT** 🚀
