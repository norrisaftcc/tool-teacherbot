# AlgoCratic TA Systems: Alpha Deployment

**Two-System Architecture for AI-Assisted Capstone Education**

---

## What This Is

A dual-system approach to providing students with AI assistance:

- **System 1**: Flask web chat interface for Q&A and debugging help
- **System 2**: Claude Code CLI distribution with pedagogical guardrails

Both systems track token usage, inject per-group context, and enforce pedagogical best practices.

---

## Quick Start: Deploying with Two Claude Code Instances

### Prerequisites
```bash
# Clone this repository
git clone [repo-url]
cd ta-systems-alpha

# Verify structure
ls -la
# Should see: system1-flask-chat/ system2-code-distribution/ shared/ docs/
```

### Launch Instance A (System 1 - Flask Chat)
```bash
# In one terminal/Claude Code session
cd system1-flask-chat

# Start Claude Code
claude-code

# First prompt:
"I'm working on System 1 - the Flask chat interface. 
Please read CLAUDE.md in this directory, then tell me what I should build first."
```

### Launch Instance B (System 2 - Distribution)
```bash
# In another terminal/Claude Code session
cd system2-code-distribution

# Start Claude Code
claude-code

# First prompt:
"I'm working on System 2 - the Claude Code distribution framework.
Please read CLAUDE.md in this directory, then tell me what I should build first."
```

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                   SYSTEM ARCHITECTURE                     │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  SYSTEM 1: Flask Web Chat Interface                      │
│  ┌────────────────────────────────────────────────┐     │
│  │ Student Login → Context Injection → Claude API │     │
│  │       ↓               ↓                  ↓      │     │
│  │   Per-Group    Pedagogical      Conversation   │     │
│  │     Auth       Guardrails         Logging      │     │
│  └────────────────────────────────────────────────┘     │
│                                                           │
│  SYSTEM 2: Claude Code CLI Distribution                  │
│  ┌────────────────────────────────────────────────┐     │
│  │ API Key Distribution → Spend Caps → CLAUDE.md  │     │
│  │         ↓                    ↓            ↓     │     │
│  │    Per-Group         Anthropic      Pedagogical │     │
│  │    Setup             Console        Guardrails  │     │
│  └────────────────────────────────────────────────┘     │
│                                                           │
│  Integration: Shared database schema, context format     │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## Timeline (24-Hour Sprint)

### Hour 0: Kickoff
- [ ] Clone repository
- [ ] Launch both Claude Code instances
- [ ] Both instances read their CLAUDE.md files
- [ ] Coordinate on shared file structure

### Hours 0-8: Parallel Core Development
**Instance A (System 1)**:
- Flask skeleton + Claude API integration
- Database models and migrations
- Basic chat interface

**Instance B (System 2)**:
- Setup script (`setup.py`)
- CLAUDE.md template system
- Config generation automation

### Hours 8-16: Integration & Features
**Instance A (System 1)**:
- Admin dashboard
- Group context loading
- Render deployment config

**Instance B (System 2)**:
- Complete documentation (instructor + student)
- Spend cap mechanism
- End-to-end testing

### Hours 16-20: Polish & Deploy
**Both Instances**:
- Security review
- Error handling
- Documentation review
- Final integration testing

### Hours 20-24: Alpha Launch
- Deploy System 1 to Render
- Distribute System 2 to first test group
- Monitor and fix critical issues

---

## Coordination Protocol

### Shared Files (`shared/` directory)
- `database_schema.sql` - Database structure (Instance A owns, Instance B reads)
- `group_context_template.md` - Context format (both use same format)
- `integration_plan.md` - Coordination notes

### Branch Naming
- Instance A: `system1/feature-name`
- Instance B: `system2/feature-name`
- Shared: Both review PRs before merging

### Communication
- Use GitHub issues for blockers
- Use PR comments for coordination
- Use `coordination` label for cross-system changes

---

## What Each System Delivers

### System 1 Outputs
```
system1-flask-chat/
├── app.py                   # Flask application
├── auth.py                  # Group authentication
├── claude_handler.py        # Claude API integration
├── models.py                # Database models
├── requirements.txt         # Python dependencies
├── render.yaml              # Deployment config
├── templates/
│   ├── login.html          # Login page
│   ├── chat.html           # Chat interface
│   └── admin.html          # Instructor dashboard
├── static/
│   └── css/terminal.css    # AlgoCratic styling
└── context/
    ├── group_1_context.md  # Per-group context files
    ├── group_2_context.md
    └── ...
```

**Deployment**: Render.com (Flask app + PostgreSQL)

### System 2 Outputs
```
system2-code-distribution/
├── setup.py                        # Group config generator
├── check_budget.py                 # Token budget checker
├── config_templates/
│   └── CLAUDE_template.md         # CLAUDE.md template
├── documentation/
│   ├── instructor_guide.md        # Setup and distribution guide
│   └── student_guide.md           # Usage guide
└── [Generated after setup.py runs]:
    ├── group_1/
    │   ├── .anthropic-key         # API key
    │   ├── spend_cap.json         # Budget config
    │   ├── CLAUDE.md              # Customized template
    │   └── README.md              # Group-specific setup
    ├── group_2/
    └── ...
```

**Distribution**: Instructor runs `setup.py`, distributes folders to groups

---

## Instructor Workflow (After Deployment)

### 1. System 1 Setup (Flask Chat)
```bash
# Deploy to Render
# Set environment variables in Render dashboard:
# - ANTHROPIC_API_KEY
# - FLASK_SECRET_KEY
# - ADMIN_PASSWORD

# Create group context files
cd system1-flask-chat/context
cp group_template.md group_1_context.md
# Edit with group 1's project details
# Repeat for all groups

# Test login with group credentials
open https://your-app.onrender.com/login
```

### 2. System 2 Setup (Claude Code Distribution)
```bash
# Generate configurations
cd system2-code-distribution
python setup.py --groups 5 --budget 100000

# Customize CLAUDE.md files
cd group_1
# Edit CLAUDE.md with group 1's project details
# Repeat for all groups

# Distribute to students
# Option A: Secure email with folder as .zip
# Option B: Private GitHub repo per group
```

### 3. Monitor Usage
```bash
# System 1 admin dashboard
open https://your-app.onrender.com/admin

# View:
# - Token usage per group
# - Recent conversations
# - Which groups need support
```

---

## Student Workflow

### Using System 1 (Web Chat)
1. Navigate to System 1 URL
2. Log in with group credentials
3. Ask questions about their project
4. Claude responds with context-aware guidance
5. Conversation logged for instructor review

**Use System 1 for**:
- Conceptual questions ("How does Flask sessions work?")
- Debugging help ("My route is returning 404")
- Architecture guidance ("Should we use Redis or SQLite?")
- Quick clarifications

### Using System 2 (Claude Code)
1. Add API key to environment
2. Copy CLAUDE.md to project repository
3. Run `claude-code` in project directory
4. Claude Code reads CLAUDE.md for context and guardrails
5. Iterate on code with AI assistance

**Use System 2 for**:
- Generating boilerplate code
- Implementing planned features
- Refactoring existing code
- Writing tests

---

## Reference Documents

### Planning
- `TA_SYSTEMS_PARALLEL_PLAN.md` - Complete parallel development plan
- `TA_SYSTEM_MVP_PLAN.md` - Original MVP architecture plan

### System 1 (Instance A)
- `system1-flask-chat/CLAUDE.md` - Instance A's guide
- Referenced repos: `algorithm-shodann` (pedagogical patterns), `tool-algoflow-py` (session management)

### System 2 (Instance B)
- `system2-code-distribution/CLAUDE.md` - Instance B's guide
- Referenced repos: `algorithm-shodann` (CLAUDE.md patterns)

---

## Troubleshooting

### Both Instances Modifying Same File
**Symptom**: Merge conflict in `shared/` directory
**Solution**: 
1. One instance creates PR first
2. Other instance reviews and approves
3. First instance merges
4. Second instance pulls and rebases

### System 1 Can't Connect to Claude API
**Symptom**: Error on chat message
**Solution**: 
- Check ANTHROPIC_API_KEY in Render dashboard
- Verify API key is valid
- Check Anthropic console for rate limits

### System 2 Students Can't Set API Key
**Symptom**: Claude Code says "No API key found"
**Solution**:
- Verify students added to environment correctly
- Check shell profile file (.bashrc, .zshrc)
- Test with: `echo $ANTHROPIC_API_KEY`

---

## Success Criteria

### Alpha Phase Success
- ✅ System 1 deployed on Render and accessible
- ✅ All 5 groups can authenticate to System 1
- ✅ System 2 configurations generated and distributed
- ✅ Students using Claude Code with guardrails
- ✅ Token tracking accurate in both systems
- ✅ Instructor can monitor usage via admin dashboard
- ✅ No critical bugs in first 48 hours

---

## Next Steps After Alpha

### System 1 Enhancements
- Conversation search and filtering
- Real-time token spend display
- Growth velocity tracking (connect to GitHub commits)
- Multiple clearance level support

### System 2 Enhancements
- Automated webhook logging to System 1
- Budget warning notifications
- Usage analytics per student
- Integration with GitHub Classroom

### Integration Enhancements
- Single sign-on across both systems
- Unified token budget tracking
- Cross-system conversation history
- AI agent specialization (different personas for different question types)

---

## Contact & Support

**For Technical Issues**:
- Create GitHub issue with `bug` label
- Include: system (1 or 2), error message, steps to reproduce

**For Pedagogical Questions**:
- Review `algorithm-shodann/design_docs/SHODANN_VOICE_GUIDE.md`
- Check AlgoCratic curriculum materials

**For Deployment Help**:
- Review `docs/deployment.md` (created by instances)
- Check Render documentation

---

**frotz → plugh**

The Algorithm provides. The Algorithm watches. The Algorithm ships.
