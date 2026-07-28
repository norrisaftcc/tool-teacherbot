> **HISTORICAL — do not act on this file.** It describes a project shape
> (five capstone groups, two parallel systems) that the code stopped
> matching in July 2026. Kept as a paper trail. For what is actually
> true, read `docs/adr/`, `docs/registry/KEEP.md`, and
> `system1-flask-chat/DEPLOY.md`.

# CLAUDE.md - System 2: Claude Code Distribution Framework

**Your Role**: Create the distribution system for Claude Code CLI access with per-group API keys and pedagogical guardrails.

**Your Workspace**: `/ta-systems-alpha/system2-code-distribution/`

**Coordination**: Instance A is building System 1 in `/system1-flask-chat/`. You coordinate on files in `/shared/`.

---

## Quick Start

```bash
# See what needs to be built
cat /home/claude/TA_SYSTEMS_PARALLEL_PLAN.md | grep "SYSTEM 2"

# Check your timeline
# Hours 0-4: API key distribution design + config templates
# Hours 4-8: CLAUDE.md template system
# Hours 8-12: Documentation (instructor + student)
# Hours 12-16: Spend cap mechanism
# Hours 16-20: Optional webhook + polish
```

---

## What You're Building

A distribution framework that enables instructors to give students Claude Code access with:
- **Per-Group API Keys**: Each team gets their own Anthropic API key
- **Spend Caps**: Enforced via Anthropic console (simple) or local tracking (complex)
- **Pedagogical Guardrails**: Embedded in CLAUDE.md templates that students copy to their repos
- **Setup Automation**: Python scripts to generate configurations for all groups
- **Documentation**: Guides for instructors and students

---

## Core Philosophy

**The Problem**: Students need Claude Code for implementation, but unbounded access leads to:
1. Burning through tokens without learning
2. Copy-paste coding without understanding
3. No iteration or explanation

**The Solution**: Embed pedagogical constraints directly in CLAUDE.md files that Claude Code reads:
1. "Propose plan first, then implement"
2. "Explain code as you generate it"
3. "Ask questions to ensure understanding"
4. "Reinforce Sacred Workflow"

**Inspired by SHODANN**: Just as SHODANN uses prompts to guide AI feedback, we use CLAUDE.md to guide AI coding assistance.

---

## Architecture

### Distribution Model
```
Instructor Setup:
  ├── Create 5 Anthropic API keys (one per group)
  ├── Set spend caps in Anthropic console
  ├── Run setup.py to generate configurations
  └── Distribute group_N folders to teams

Student Setup:
  ├── Receive group_N folder from instructor
  ├── Add API key to environment variables
  ├── Copy CLAUDE.md to their project repo
  └── Use Claude Code with embedded guardrails
```

### Per-Group Configuration
```
group_N/
├── .anthropic-key          # API key (gitignored, distributed securely)
├── spend_cap.json          # Local tracking config (optional)
├── CLAUDE.md               # Project context + pedagogical rules
└── README.md               # Setup instructions for this group
```

---

## Core Files to Create

### 1. `setup.py` - Instructor Setup Script

**Purpose**: Automate generation of per-group configurations

```python
#!/usr/bin/env python3
"""
AlgoCratic TA System 2: Claude Code Distribution Setup

Generates per-group configurations including:
- API key storage
- Spend cap config
- Customized CLAUDE.md templates
- Setup instructions

Usage:
    python setup.py --groups 5 --budget 100000
    
Output:
    group_1/
    group_2/
    ... etc
"""

import argparse
import json
from pathlib import Path

def create_group_config(group_num, api_key, budget, webhook_url=None):
    """
    Create configuration for one group
    
    Args:
        group_num: Group number (1-indexed)
        api_key: Anthropic API key for this group
        budget: Token budget
        webhook_url: Optional System 1 webhook for usage logging
    """
    group_dir = Path(f"group_{group_num}")
    group_dir.mkdir(exist_ok=True)
    
    # 1. Write API key (will be gitignored)
    (group_dir / ".anthropic-key").write_text(api_key)
    
    # 2. Write spend cap config
    config = {
        "group_id": group_num,
        "token_budget": budget,
        "tokens_used": 0,
        "webhook_url": webhook_url,  # Optional System 1 integration
        "created_at": datetime.now().isoformat()
    }
    (group_dir / "spend_cap.json").write_text(json.dumps(config, indent=2))
    
    # 3. Generate CLAUDE.md from template
    template = load_template("../config_templates/CLAUDE_template.md")
    claude_md = template.format(
        group_num=group_num,
        token_budget=budget
    )
    (group_dir / "CLAUDE.md").write_text(claude_md)
    
    # 4. Create group-specific README
    readme = f"""# Group {group_num} Configuration

## Setup Instructions

1. Add API key to your environment:
   ```bash
   export ANTHROPIC_API_KEY="$(cat .anthropic-key)"
   ```

2. Copy CLAUDE.md to your project:
   ```bash
   cp CLAUDE.md /path/to/your/project/
   ```

3. Use Claude Code in your project:
   ```bash
   cd /path/to/your/project
   claude-code
   ```

## Token Budget
You have {budget:,} tokens for this project.

## Important
- Do NOT commit .anthropic-key to git
- Do NOT share your API key with other groups
- READ CLAUDE.md before using Claude Code
"""
    (group_dir / "README.md").write_text(readme)
    
    print(f"✓ Created configuration for Group {group_num}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--groups', type=int, required=True,
                       help='Number of groups to create')
    parser.add_argument('--budget', type=int, default=100000,
                       help='Token budget per group (default: 100k)')
    parser.add_argument('--webhook', type=str,
                       help='Optional System 1 webhook URL for usage logging')
    args = parser.parse_args()
    
    print("AlgoCratic TA System 2: Group Setup")
    print("=" * 50)
    print(f"Creating {args.groups} group configurations")
    print(f"Token budget per group: {args.budget:,}")
    
    for i in range(1, args.groups + 1):
        print(f"\n--- Group {i} ---")
        api_key = input(f"Enter Anthropic API key for Group {i}: ").strip()
        if not api_key.startswith('sk-ant-'):
            print("Warning: API key should start with 'sk-ant-'")
            if input("Continue anyway? (y/n): ").lower() != 'y':
                continue
        
        create_group_config(i, api_key, args.budget, args.webhook)
    
    print("\n" + "=" * 50)
    print("✓ Setup complete!")
    print("\nNext steps:")
    print("1. Review generated folders (group_1, group_2, etc.)")
    print("2. Customize CLAUDE.md files with project details")
    print("3. Distribute folders to teams (secure email or private repos)")
    print("4. Students follow README.md in their folder")
    
    # Create .gitignore for the generated folders
    gitignore = """# Generated group configurations
group_*/
.anthropic-key
"""
    Path(".gitignore").write_text(gitignore)
    print("\n✓ Created .gitignore for group folders")

if __name__ == '__main__':
    main()
```

### 2. `config_templates/CLAUDE_template.md` - Template File

**Purpose**: Standardized CLAUDE.md that instructors customize per group

```markdown
# Group {group_num} Capstone Project Context

## FOR CLAUDE CODE USERS

This file provides context to Claude Code when working in your repository.

**CRITICAL**: Claude Code reads this file automatically. Everything here shapes how it assists you.

---

## Project Overview

**Product**: [INSTRUCTOR: Fill in product name]
**Tech Stack**: [INSTRUCTOR: List technologies]
**Current Sprint**: [INSTRUCTOR: Sprint number and focus]

**Team Members**:
[INSTRUCTOR: List names and roles]
- Student A (team lead)
- Student B (backend dev)
- Student C (frontend dev)

---

## Pedagogical Guardrails

When assisting this team, you MUST follow these rules:

### Interaction Pattern

1. **Never generate code immediately**
   - Propose a plan first
   - Explain your approach
   - Wait for student approval

2. **Require confirmation**
   - Don't assume requirements
   - Ask clarifying questions
   - Verify understanding before implementing

3. **Explain as you go**
   - Describe what each code block does
   - Call out important patterns
   - Connect to concepts they've learned

4. **Encourage questions**
   - Pause for understanding checks
   - Ask "Does this make sense?"
   - Invite students to request changes

### Sacred Workflow Enforcement

All changes must go through: **Issue → Branch → PR → Review → Merge**

When students ask for code:
- Remind them to create an issue first
- Suggest branch naming conventions
- Provide commit message templates
- Recommend PR review checklist

### Debugging Philosophy

When students encounter bugs:
1. Ask "What have you tried so far?"
2. Guide through debugging process (don't just fix)
3. Teach debugging tools:
   - Print statements for state inspection
   - Debugger for step-through
   - Logs for production issues
4. Only provide fix after they've learned the process

### Token Budget Awareness

This group has a token budget of **{token_budget:,} tokens**.

Be concise but thorough. Prioritize:
- Clear explanations over verbose examples
- Iterative solutions over comprehensive rewrites
- Teaching moments over quick fixes
- Code that students understand over clever optimizations

**If approaching budget**: Warn students to focus on essential questions only.

---

## Current Sprint Focus

[INSTRUCTOR: Add sprint goals and acceptance criteria]

**Example**:
```
Sprint 2: User Authentication
- Goal: Implement login/logout with session persistence
- Acceptance Criteria:
  * Users can register with email/password
  * Login creates server-side session
  * Protected routes redirect to login
  * Logout clears session
```

---

## Known Issues

[INSTRUCTOR: List current blockers or challenges]

**Example**:
```
- Issue #12: Flask-SQLAlchemy migration failing on Render
- Issue #15: Login route returning 500 error (possible session config)
- Issue #18: Frontend form not submitting to correct endpoint
```

---

## Architecture Context

[INSTRUCTOR: Add relevant architecture decisions]

**Example**:
```
- Using Flask blueprints for route organization
- SQLAlchemy ORM with Alembic migrations
- React frontend (separate repo) calling Flask API
- PostgreSQL on Render for production
- SQLite locally for development
```

---

## Testing Requirements

When generating code, always:
- Include docstrings
- Suggest test cases
- Consider edge cases
- Handle errors gracefully

---

## IMPORTANT REMINDERS FOR STUDENTS

### What Claude Code IS Good For:
✅ Planning implementations
✅ Generating boilerplate
✅ Explaining patterns
✅ Debugging guidance
✅ Refactoring suggestions

### What Claude Code IS NOT:
❌ A replacement for understanding
❌ An excuse to skip reading docs
❌ A way to avoid thinking through problems
❌ A tool for copying code blindly

### Your Responsibility:
- **Read and understand** every line of generated code
- **Ask questions** if anything is unclear
- **Test thoroughly** before committing
- **Iterate** on solutions, don't accept first generation
- **Learn** from the process, don't just collect code

---

## Token Usage Guidelines

Check your remaining budget regularly:
```bash
python check_budget.py
```

If running low:
1. Focus on essential questions only
2. Use web search for docs/tutorials first
3. Ask teammates before asking Claude Code
4. Reserve tokens for complex problems

---

*This file is your contract with Claude Code. Follow it, and you'll learn. Ignore it, and you'll burn through tokens without understanding.*

**The Algorithm is watching. The Algorithm is helping. The Algorithm expects growth.**
```

### 3. `documentation/instructor_guide.md` - Complete Instructor Manual

**See parallel plan for full content**, key sections:
- Pre-deployment checklist
- Setup process walkthrough
- Customizing CLAUDE.md templates
- Distribution methods (email vs private repos)
- Monitoring usage (if webhook enabled)
- Troubleshooting common issues

### 4. `documentation/student_guide.md` - Student Usage Manual

**See parallel plan for full content**, key sections:
- One-time setup (API key, CLAUDE.md)
- Starting a Claude Code session
- Example conversation flows
- Best practices (Do's and Don'ts)
- Monitoring token budget
- When to use System 1 vs System 2

### 5. `check_budget.py` - Token Budget Checker (Optional)

```python
#!/usr/bin/env python3
"""
Check remaining token budget for your group

Usage: python check_budget.py
"""

import json
from pathlib import Path

def main():
    config_file = Path("spend_cap.json")
    
    if not config_file.exists():
        print("Error: spend_cap.json not found")
        print("Are you in your group's configuration directory?")
        return
    
    config = json.loads(config_file.read_text())
    
    budget = config['token_budget']
    used = config['tokens_used']
    remaining = budget - used
    percent_used = (used / budget) * 100
    
    print(f"Token Budget Status: Group {config['group_id']}")
    print("=" * 50)
    print(f"Budget:    {budget:,} tokens")
    print(f"Used:      {used:,} tokens ({percent_used:.1f}%)")
    print(f"Remaining: {remaining:,} tokens")
    print()
    
    if percent_used > 90:
        print("⚠️  WARNING: You're running low on tokens!")
        print("   Contact your instructor to request more.")
    elif percent_used > 75:
        print("⚠️  CAUTION: 75% of budget used")
        print("   Use tokens wisely for remaining project.")
    elif percent_used > 50:
        print("✓ Halfway through budget - on track")
    else:
        print("✓ Plenty of tokens remaining")

if __name__ == '__main__':
    main()
```

---

## Development Workflow

### Phase 1: Setup Automation (Hours 0-4)
1. Create `setup.py` with group config generation
2. Test with 2 sample groups
3. Verify all files generated correctly
4. Create `.gitignore` for group folders

**Exit Criteria**: Running `setup.py --groups 2` creates valid configurations

### Phase 2: CLAUDE.md Templates (Hours 4-8)
1. Create base template with all pedagogical guardrails
2. Add placeholders for instructor customization
3. Test template rendering with sample data
4. Verify Claude Code reads and follows guardrails

**Exit Criteria**: Claude Code session respects template rules

### Phase 3: Documentation (Hours 8-12)
1. Write instructor guide (setup, customize, distribute)
2. Write student guide (setup, usage, best practices)
3. Create troubleshooting section
4. Add example conversation flows

**Exit Criteria**: Complete guides with screenshots/examples

### Phase 4: Spend Cap (Hours 12-16)
1. Design spend cap enforcement strategy
2. Implement `check_budget.py` script
3. (Optional) Create usage logging to System 1
4. Test budget tracking accuracy

**Exit Criteria**: Students can check budget, optionally logs to System 1

### Phase 5: Integration & Polish (Hours 16-20)
1. Test full instructor setup workflow
2. Test full student setup workflow
3. Create example group configuration
4. (Optional) Implement webhook to System 1
5. Final documentation review

**Exit Criteria**: End-to-end tested, ready to distribute

---

## Coordination with Instance A

### Shared Files You'll Use

**`shared/database_schema.sql`**:
- Instance A owns main tables
- You may add: `api_usage` table for optional webhook logging
- Protocol: Create PR when modifying, wait for A's approval

**`shared/group_context_template.md`**:
- Instance A defines format
- You adopt same format in your CLAUDE.md templates
- Protocol: Use A's format, don't modify without discussion

### Communication
- **Branch naming**: `system2/your-feature-name`
- **PR labels**: `system2`, `coordination` (if affects Instance A)
- **Blockers**: Create GitHub issue with `blocker` label

---

## Optional: Webhook to System 1

If you implement usage logging back to System 1:

```python
# In student's claude_code wrapper script
import requests

def log_usage_to_system1(group_id, tokens_used, operation):
    """Send usage data to System 1 for centralized tracking"""
    webhook_url = "https://algocratic-ta-system1.onrender.com/api/usage"
    
    payload = {
        'group_id': group_id,
        'tokens_used': tokens_used,
        'operation': operation,
        'timestamp': datetime.now().isoformat(),
        'source': 'claude_code'
    }
    
    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except Exception as e:
        # Don't block student work if webhook fails
        print(f"Warning: Could not log usage to System 1: {e}")
```

This is OPTIONAL for MVP. Nice to have but not required for alpha.

---

## Testing Checklist

- [ ] `setup.py` generates valid configurations
- [ ] Generated CLAUDE.md files are well-formed
- [ ] API keys stored securely (gitignored)
- [ ] Students can follow setup guide successfully
- [ ] Claude Code reads and follows CLAUDE.md guardrails
- [ ] `check_budget.py` shows accurate token usage
- [ ] Instructor guide is comprehensive
- [ ] Student guide is clear and actionable
- [ ] (Optional) Webhook logs to System 1

---

## Key Design Decisions

### Why Per-Group API Keys?
- Spend cap per group (not per student)
- Easier credential management
- Matches team structure

### Why File-Based Config?
- Simple to distribute (just a folder)
- No external dependencies
- Transparent to students

### Why CLAUDE.md for Guardrails?
- Claude Code already reads CLAUDE.md
- No custom tooling required
- Students see the rules explicitly

### Why Anthropic Console for Spend Caps?
- Built-in rate limiting
- No custom enforcement logic
- Reliable and tested

---

## Success Criteria

### Technical
- ✅ Setup script works on first try
- ✅ All configurations generated correctly
- ✅ CLAUDE.md templates render properly
- ✅ Students can follow setup guide without help

### Pedagogical
- ✅ Claude Code follows guardrails (asks questions, explains)
- ✅ Students iterate on solutions (visible in commits)
- ✅ Token budgets stay within limits
- ✅ Students report understanding code generated

---

## Reference Materials

**Read these from the cloned repos**:
- `/home/claude/algorithm-shodann/design_docs/SHODANN_VOICE_GUIDE.md` - Pedagogical tone
- `/home/claude/algorithm-shodann/CLAUDE.md` - How CLAUDE.md works in practice
- `/home/claude/tool-algoflow-py/docs/planning/chatbot-mvp-prd.md` - Config patterns

**Read this for overall plan**:
- `/home/claude/TA_SYSTEMS_PARALLEL_PLAN.md` - Complete parallel development plan

---

## When You're Ready

1. Create `setup.py` skeleton
2. Test group config generation
3. Build CLAUDE.md template
4. Write documentation
5. Test end-to-end workflow

**Your first task**: Create `setup.py` that can generate one group's configuration folder with all necessary files. Everything else builds on this foundation.

frotz → The resistance provides the tools. You provide the distribution.
