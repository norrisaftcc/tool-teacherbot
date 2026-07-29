> **HISTORICAL — do not act on this file.** It describes a project shape
> (five capstone groups, two parallel systems) that the code stopped
> matching in July 2026. Kept as a paper trail. For what is actually
> true, read `docs/adr/`, `docs/registry/KEEP.md`, and
> `system1-flask-chat/DEPLOY.md`.

# TA System Alpha: Parallel Development Plan
## Two Claude Code Instances, 24-Hour Deployment

**Context**: Build System 1 (Flask chat interface) and System 2 (Claude Code CLI distribution) as separate but integrated components, inspired by SHODANN's pedagogical philosophy and the PocketFlow chatbot architecture.

---

## ARCHITECTURE OVERVIEW

```
┌──────────────────────────────────────────────────────────────┐
│                     SYSTEM ARCHITECTURE                       │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  SYSTEM 1: Flask Web Chat                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Student Login → Claude Context → Conversation Log   │    │
│  │       ↓              ↓                  ↓            │    │
│  │   Per-Group    Pedagogical      Token Tracking      │    │
│  │     Auth       Guardrails       & Logging           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
│  SYSTEM 2: Claude Code CLI Distribution                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Per-Group API Keys → Spend Caps → CLAUDE.md        │    │
│  │       ↓                   ↓             ↓            │    │
│  │  Distribution      Usage Logging   Pedagogical      │    │
│  │   Framework        (optional)      Guardrails       │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Integration Point**: Both systems log to same database (System 1 required, System 2 optional webhook)

**Inspired by**:
- SHODANN's growth velocity philosophy and pedagogical guardrails
- PocketFlow's session management and API design patterns
- AlgoCratic clearance-based context injection

---

## REPOSITORY STRUCTURE

```
ta-systems-alpha/
├── system1-flask-chat/          # Instance A works here
│   ├── app.py
│   ├── auth.py
│   ├── claude_handler.py
│   ├── models.py
│   ├── requirements.txt
│   ├── templates/
│   ├── static/
│   ├── context/
│   └── CLAUDE.md
│
├── system2-code-distribution/   # Instance B works here
│   ├── README.md
│   ├── setup.py
│   ├── config_templates/
│   ├── documentation/
│   └── CLAUDE.md
│
├── shared/                      # Coordination point
│   ├── database_schema.sql
│   ├── group_context_template.md
│   └── integration_plan.md
│
└── docs/
    ├── deployment.md
    ├── instructor_guide.md
    └── student_guide.md
```

---

## CLAUDE CODE INSTANCE A: SYSTEM 1 - FLASK CHAT

### Your Mission
Build a Flask web application that provides authenticated, context-aware Claude access with conversation logging and token tracking.

### Your Workspace
`/ta-systems-alpha/system1-flask-chat/`

### Your CLAUDE.md Context
See `/ta-systems-alpha/system1-flask-chat/CLAUDE.md` (created below)

### Success Criteria
- [ ] Students can log in with group credentials
- [ ] Claude conversations include group-specific context
- [ ] All conversations logged to database
- [ ] Token usage tracked per group
- [ ] Deployable to Render with one click
- [ ] Admin dashboard shows usage and logs

### Key Inspiration Sources
- **Session Management**: tool-algoflow-py's chatbot PRD pattern
- **Pedagogical Guardrails**: SHODANN's prompt structure and voice guide
- **Context Injection**: Per-group context files like SHODANN's clearance system

### Timeline
**Hours 0-4**: Core Flask + Claude API integration
**Hours 4-8**: Database + conversation logging
**Hours 8-12**: Admin dashboard + group context loading
**Hours 12-16**: Render deployment config + testing
**Hours 16-20**: Polish + documentation

### No-Conflict Zones
- You own everything in `system1-flask-chat/`
- You coordinate on `shared/` files (read, propose changes, wait for merge)
- Instance B handles everything in `system2-code-distribution/`

---

## CLAUDE CODE INSTANCE B: SYSTEM 2 - CODE DISTRIBUTION

### Your Mission
Create a Claude Code CLI distribution framework with per-group API keys, spend caps, and pedagogical guardrails embedded in CLAUDE.md templates.

### Your Workspace
`/ta-systems-alpha/system2-code-distribution/`

### Your CLAUDE.md Context
See `/ta-systems-alpha/system2-code-distribution/CLAUDE.md` (created below)

### Success Criteria
- [ ] Per-group API key configuration system
- [ ] Spend cap enforcement mechanism
- [ ] CLAUDE.md template generator (per-group customization)
- [ ] Instructor setup guide
- [ ] Student usage guide
- [ ] Optional: Usage webhook back to System 1

### Key Inspiration Sources
- **Pedagogical Constraints**: SHODANN's prompt layers and voice guide
- **State Management**: SHODANN's file-based config pattern
- **Distribution Model**: Render environment variable approach

### Timeline
**Hours 0-4**: API key distribution design + config templates
**Hours 4-8**: CLAUDE.md template system
**Hours 8-12**: Documentation (instructor + student)
**Hours 12-16**: Spend cap mechanism + testing
**Hours 16-20**: Optional webhook + polish

### No-Conflict Zones
- You own everything in `system2-code-distribution/`
- You coordinate on `shared/` files (read, propose changes, wait for merge)
- Instance A handles everything in `system1-flask-chat/`

---

## COORDINATION PROTOCOL

### Shared File Changes
When you need to modify anything in `shared/`:

1. **Pull latest**: `git pull origin main`
2. **Create branch**: `git checkout -b system1/shared-schema-update` (or `system2/...`)
3. **Make changes**: Edit the shared file
4. **Commit**: `git commit -m "System 1: Update database schema for token tracking"`
5. **Push**: `git push origin system1/shared-schema-update`
6. **PR**: Create PR, notify other instance
7. **Wait for approval**: Other instance reviews and approves
8. **Merge**: Once approved, merge and delete branch

### Communication via Git
- **System 1 updates**: Use `system1/` branch prefix
- **System 2 updates**: Use `system2/` branch prefix
- **Shared concerns**: Both instances comment on PRs
- **Blockers**: Use GitHub issues with `coordination` label

### Integration Points

**Database Schema** (`shared/database_schema.sql`):
- System 1 owns: `groups`, `conversations`, `messages` tables
- System 2 reads: `groups` table for API key mapping
- System 2 writes (optional): `api_usage` table for Claude Code logging

**Group Context Template** (`shared/group_context_template.md`):
- Both systems use the same format
- System 1 loads these for Claude conversations
- System 2 embeds these in CLAUDE.md templates

---

## SYSTEM 1 DETAILED SPEC

### Tech Stack
```
Flask 3.x
├── Flask-Login (authentication)
├── Flask-Session (server-side sessions)  
├── Anthropic SDK (Claude API)
├── SQLite (dev) / PostgreSQL (Render)
└── Python 3.11+
```

### Core Files

**`app.py`** - Main Flask application
```python
from flask import Flask, render_template, session
from anthropic import Anthropic

app = Flask(__name__)
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

@app.route('/chat', methods=['POST'])
def chat():
    group_id = session['group_id']
    user_message = request.json['message']
    
    # Load group context
    context = load_group_context(group_id)
    
    # Call Claude with context
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=build_system_prompt(context),
        messages=get_conversation_history(group_id) + [
            {"role": "user", "content": user_message}
        ]
    )
    
    # Log conversation
    log_message(group_id, "user", user_message, 0)
    log_message(group_id, "assistant", response.content[0].text, 
                response.usage.input_tokens + response.usage.output_tokens)
    
    return jsonify(response.content[0].text)
```

**`auth.py`** - Group-based authentication
```python
GROUPS = {
    'group1': {'password': 'capstone2026', 'clearance': 'ORANGE'},
    'group2': {'password': 'dataman2026', 'clearance': 'YELLOW'},
    # ... etc
}

@app.route('/login', methods=['POST'])
def login():
    group_id = request.form['group_id']
    password = request.form['password']
    
    if group_id in GROUPS and GROUPS[group_id]['password'] == password:
        session['group_id'] = group_id
        session['clearance'] = GROUPS[group_id]['clearance']
        return redirect('/chat')
    else:
        return render_template('login.html', error='Invalid credentials')
```

**`claude_handler.py`** - Context injection and prompt building
```python
def build_system_prompt(group_context):
    """Build pedagogical system prompt with group context"""
    return f"""You are an AI teaching assistant for AlgoCratic Futures capstone course.

CURRENT GROUP CONTEXT:
{group_context}

PEDAGOGICAL RULES:
1. Never provide direct solutions - guide through iterative problem-solving
2. Require students to explain their current attempt first
3. Ask clarifying questions before answering
4. Emphasize the Sacred Workflow (Issue → Branch → PR → Review)
5. Reference their project context when relevant
6. Celebrate iteration and learning velocity over perfection

RESPONSE STYLE:
- Technical but encouraging
- Light AlgoCratic corporate voice (5% seasoning)
- Prioritize competence building over entertainment

When a student asks for help:
1. Acknowledge their question
2. Ask what they've tried so far
3. Guide them toward the solution iteratively
4. Reference their project context when relevant
"""

def load_group_context(group_id):
    """Load group-specific context file"""
    context_file = f'context/group_{group_id}_context.md'
    with open(context_file, 'r') as f:
        return f.read()
```

**`models.py`** - Database models
```python
from datetime import datetime

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    clearance_level = db.Column(db.String(20))
    token_budget = db.Column(db.Integer, default=100000)
    tokens_used = db.Column(db.Integer, default=0)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    started_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    role = db.Column(db.String(20))  # 'user' or 'assistant'
    content = db.Column(db.Text)
    tokens_used = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### UI Design (AlgoCratic Terminal Aesthetic)

**`templates/chat.html`**
```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/terminal.css') }}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="terminal">
        <div class="terminal-header">
            ALGOCRATIC TEACHING ASSISTANT™
            <span class="clearance">{{ session.clearance }} CLEARANCE</span>
        </div>
        <div id="conversation" class="terminal-body">
            <!-- Messages appear here -->
        </div>
        <div class="terminal-input">
            <span class="prompt">{{ session.group_id }}@algocratic:~$</span>
            <input type="text" id="message-input" autofocus>
        </div>
    </div>
</body>
</html>
```

**`static/css/terminal.css`**
```css
body {
    background: #0a0a10;
    color: #00ff00;
    font-family: 'IBM Plex Mono', monospace;
    margin: 0;
    padding: 20px;
}

.terminal {
    border: 2px solid #00ff00;
    max-width: 900px;
    margin: 0 auto;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
}

.terminal-header {
    background: #001a00;
    padding: 10px;
    border-bottom: 1px solid #00ff00;
    display: flex;
    justify-content: space-between;
}

.clearance {
    color: #ffaa00;
    font-weight: 600;
}

.terminal-body {
    padding: 20px;
    height: 500px;
    overflow-y: auto;
    background: #0a0a10;
}

.message {
    margin: 10px 0;
    padding: 10px;
    border-left: 3px solid #00ff00;
}

.message.user {
    border-left-color: #ffaa00;
}

.terminal-input {
    background: #001a00;
    padding: 10px;
    border-top: 1px solid #00ff00;
    display: flex;
    align-items: center;
}

.prompt {
    color: #ffaa00;
    margin-right: 10px;
}

input {
    background: transparent;
    border: none;
    color: #00ff00;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    flex: 1;
    outline: none;
}

input::placeholder {
    color: #006600;
}
```

### Admin Dashboard

**`templates/admin.html`**
```html
<div class="admin-dashboard">
    <h1>INSTRUCTOR DASHBOARD</h1>
    
    <section class="token-usage">
        <h2>Token Usage by Group</h2>
        <table>
            <tr>
                <th>Group</th>
                <th>Tokens Used</th>
                <th>Budget</th>
                <th>% Used</th>
            </tr>
            {% for group in groups %}
            <tr>
                <td>{{ group.name }}</td>
                <td>{{ group.tokens_used }}</td>
                <td>{{ group.token_budget }}</td>
                <td>{{ (group.tokens_used / group.token_budget * 100) | round(1) }}%</td>
            </tr>
            {% endfor %}
        </table>
    </section>
    
    <section class="recent-conversations">
        <h2>Recent Conversations</h2>
        <!-- Conversation log display -->
    </section>
</div>
```

### Render Deployment

**`render.yaml`**
```yaml
services:
  - type: web
    name: algocratic-ta-system1
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: ANTHROPIC_API_KEY
        sync: false  # Set in Render dashboard
      - key: FLASK_SECRET_KEY
        generateValue: true
      - key: ADMIN_PASSWORD
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: ta-system-db
          property: connectionString

databases:
  - name: ta-system-db
    databaseName: ta_system
    user: ta_admin
```

---

## SYSTEM 2 DETAILED SPEC

### Distribution Model

**Per-Group Configuration**
```
group_1/
├── .anthropic-key          # API key file (gitignored)
├── spend_cap.json          # Local spend tracking
└── CLAUDE.md               # Project context + guardrails
```

### Config Template Generator

**`setup.py`** - Instructor setup script
```python
#!/usr/bin/env python3
"""
AlgoCratic TA System 2: Claude Code Distribution Setup

Usage:
    python setup.py --groups 5 --budget 100000
"""

import argparse
import json
from pathlib import Path

def create_group_config(group_num, api_key, budget):
    """Create configuration for one group"""
    group_dir = Path(f"group_{group_num}")
    group_dir.mkdir(exist_ok=True)
    
    # Write API key
    (group_dir / ".anthropic-key").write_text(api_key)
    
    # Write spend cap config
    config = {
        "group_id": group_num,
        "token_budget": budget,
        "tokens_used": 0,
        "webhook_url": "https://your-system1.onrender.com/api/usage"  # Optional
    }
    (group_dir / "spend_cap.json").write_text(json.dumps(config, indent=2))
    
    # Generate CLAUDE.md from template
    template = load_template("group_context_template.md")
    claude_md = template.format(
        group_num=group_num,
        token_budget=budget
    )
    (group_dir / "CLAUDE.md").write_text(claude_md)
    
    print(f"✓ Created configuration for Group {group_num}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--groups', type=int, required=True)
    parser.add_argument('--budget', type=int, default=100000)
    args = parser.parse_args()
    
    print("AlgoCratic TA System 2: Group Setup")
    print("=" * 50)
    
    for i in range(1, args.groups + 1):
        api_key = input(f"Enter API key for Group {i}: ")
        create_group_config(i, api_key, args.budget)
    
    print("\n✓ Setup complete!")
    print("\nNext steps:")
    print("1. Distribute group_N folders to each team")
    print("2. Students add API key to their environment")
    print("3. Students read CLAUDE.md for usage guidance")

if __name__ == '__main__':
    main()
```

### CLAUDE.md Template

**`config_templates/CLAUDE_template.md`**
```markdown
# Group {group_num} Capstone Project Context

## FOR CLAUDE CODE USERS

This file provides context to Claude Code when working in your repository.

### Project Overview
[INSTRUCTOR: Fill in project details]
- Product: [Product name]
- Tech stack: [Technologies]
- Current sprint: [Sprint number and focus]

### Team Members
[INSTRUCTOR: List team members and roles]

### Pedagogical Guardrails

When assisting this team, you MUST follow these rules:

#### Interaction Pattern
1. **Never generate code immediately** - Propose a plan first
2. **Require confirmation** - Wait for student approval before implementation
3. **Explain as you go** - Describe what each code block does
4. **Encourage questions** - Pause for understanding checks

#### Sacred Workflow Enforcement
Changes must go through: Issue → Branch → PR → Review → Merge

- Remind students to create issues before branches
- Suggest commit message formats
- Recommend PR review checklist

#### Debugging Philosophy
- Ask "what have you tried?" before suggesting solutions
- Guide through debugging process, don't fix directly
- Teach debugging tools (print statements, debugger, logs)

#### Token Budget Awareness
This group has a token budget of {token_budget} tokens.

Be concise but thorough. Prioritize:
- Clear explanations over verbose examples
- Iterative solutions over comprehensive rewrites
- Teaching moments over quick fixes

### Current Sprint Focus
[INSTRUCTOR: Add sprint goals and constraints]

### Known Issues
[INSTRUCTOR: List current blockers or challenges]

---

*This file is your contract with Claude Code. Follow it, and you'll learn. Ignore it, and you'll burn through tokens without understanding.*
```

### Student Usage Guide

**`documentation/student_guide.md`**
```markdown
# Student Guide: Using Claude Code

## Setup (One-Time)

1. **Get your group's folder** from instructor
   - Contains: API key, CLAUDE.md, spend cap config

2. **Add API key to environment**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export ANTHROPIC_API_KEY="sk-ant-..."
   
   # Or for Windows (PowerShell)
   $env:ANTHROPIC_API_KEY="sk-ant-..."
   ```

3. **Copy CLAUDE.md to your project repo**
   ```bash
   cp /path/to/group_N/CLAUDE.md /path/to/your/project/
   ```

## Usage

### Starting a Session
```bash
cd /path/to/your/project
claude-code
```

Claude Code will automatically read CLAUDE.md for context.

### Example Conversation
```
You: I need to add user authentication to our Flask app.

Claude Code: Before I generate code, let me propose a plan:

1. Install Flask-Login dependency
2. Create User model with password hashing
3. Add login/logout routes
4. Protect routes with @login_required decorator

Does this approach work for your requirements?

You: Yes, but we're using SQLite, not PostgreSQL.

Claude Code: Got it. I'll adjust for SQLite. Let's start with 
the User model...
```

### Best Practices

**Do:**
- ✅ Explain what you're trying to accomplish
- ✅ Ask Claude Code to explain generated code
- ✅ Iterate on solutions
- ✅ Reference your CLAUDE.md for project context

**Don't:**
- ❌ Copy-paste code without understanding
- ❌ Skip the planning step
- ❌ Ignore Claude Code's questions
- ❌ Burn tokens on repetitive regeneration

### Monitoring Your Token Budget
Check your remaining budget:
```bash
python check_budget.py
```

### When You're Stuck
1. Read the error message carefully
2. Try debugging yourself first
3. Ask Claude Code specific questions
4. If still stuck, ask your team
5. If still stuck, use System 1 (web chat)

---

*Remember: Claude Code is a powerful tool, but learning happens 
when YOU understand the code, not when the AI writes it for you.*
```

### Instructor Setup Guide

**`documentation/instructor_guide.md`**
```markdown
# Instructor Guide: System 2 Distribution

## Pre-Deployment Checklist

- [ ] Create Anthropic API keys (one per group)
- [ ] Set spend caps via Anthropic console
- [ ] Customize CLAUDE.md template with course details
- [ ] Generate group configurations
- [ ] Test with sample project

## Setup Process

### 1. Generate Configurations
```bash
python setup.py --groups 5 --budget 100000
```

This creates:
```
group_1/
group_2/
group_3/
group_4/
group_5/
```

### 2. Customize CLAUDE.md Files
Edit each `group_N/CLAUDE.md` to include:
- Project name and tech stack
- Team member names and roles
- Current sprint focus
- Known issues or blockers

### 3. Distribute to Students
**Option A: Secure email**
- Email each team their folder contents
- Include setup instructions

**Option B: Private repo**
- Create private repo per group
- Add folder contents
- Invite team members

### 4. Monitor Usage (Optional)
If you enabled webhook logging:
- Check System 1 admin dashboard
- View token usage by group
- Identify groups needing support

## Troubleshooting

**Issue: Students running out of tokens**
- Increase budget via Anthropic console
- Update spend_cap.json
- Notify team of new limit

**Issue: Students not following guardrails**
- Review their commit history
- Check for copy-paste patterns
- Reinforce CLAUDE.md importance

**Issue: API key leaked**
- Revoke via Anthropic console
- Generate new key
- Distribute to team securely

---

*System 2 is about empowering students with AI tools while 
maintaining pedagogical integrity through embedded guardrails.*
```

---

## INTEGRATION TESTING PLAN

### Test Scenario 1: Student Workflow
1. Student logs into System 1 (Flask chat)
2. Asks question about their project
3. Receives context-aware response
4. Conversation logged with token usage
5. Student switches to Claude Code (System 2)
6. Generates code with CLAUDE.md guardrails
7. Both systems track token usage

### Test Scenario 2: Instructor Monitoring
1. Instructor views admin dashboard
2. Sees all group token usage
3. Identifies Group 3 using 80% of budget
4. Reviews Group 3's conversation logs
5. Intervenes with guidance if needed

### Test Scenario 3: Budget Enforcement
1. Group reaches 100% of token budget
2. System 1 blocks new conversations
3. System 2 (if webhook enabled) warns about limit
4. Instructor increases budget
5. Systems resume normal operation

---

## DEPLOYMENT CHECKLIST

### System 1 (Instance A)
- [ ] Flask app running locally
- [ ] Database migrations complete
- [ ] All group context files created
- [ ] Admin dashboard accessible
- [ ] Render deployment config tested
- [ ] Environment variables documented

### System 2 (Instance B)
- [ ] Setup script tested with sample data
- [ ] CLAUDE.md template validated
- [ ] Student guide reviewed
- [ ] Instructor guide complete
- [ ] Optional webhook tested

### Integration
- [ ] Database schema coordinated
- [ ] Group context format agreed
- [ ] Token tracking verified
- [ ] Both systems deployed
- [ ] End-to-end test completed

---

## SUCCESS METRICS (Alpha Phase)

### System 1
- ✅ All 5 groups can authenticate
- ✅ Conversations include project context
- ✅ Token tracking accurate within 1%
- ✅ Admin dashboard shows real-time data
- ✅ Response time <3 seconds

### System 2
- ✅ All groups receive API keys
- ✅ CLAUDE.md templates customized
- ✅ Students follow setup guide successfully
- ✅ Pedagogical guardrails observable in commits
- ✅ Token usage stays within budgets

### Integration
- ✅ No data conflicts
- ✅ Consistent token tracking
- ✅ Instructor can monitor both systems
- ✅ Students use both systems effectively

---

## HANDOFF TO CLAUDE CODE INSTANCES

### For Instance A (System 1)
1. Clone repository
2. `cd ta-systems-alpha/system1-flask-chat`
3. Read `CLAUDE.md` in that directory
4. Start with: "I'm working on System 1. What should I build first?"

### For Instance B (System 2)
1. Clone repository
2. `cd ta-systems-alpha/system2-code-distribution`
3. Read `CLAUDE.md` in that directory
4. Start with: "I'm working on System 2. What should I build first?"

---

**Ready to deploy. The resistance awaits your signal.**

frotz → plugh
