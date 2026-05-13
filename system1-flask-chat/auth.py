from pathlib import Path

# Alpha: hardcoded credentials. Replace with DB-backed auth post-alpha.
GROUPS = {
    'group1': {'password': 'capstone2026', 'clearance': 'ORANGE'},
    'group2': {'password': 'dataman2026',  'clearance': 'YELLOW'},
    'group3': {'password': 'finaid2026',   'clearance': 'ORANGE'},
    'group4': {'password': 'health2026',   'clearance': 'YELLOW'},
    'group5': {'password': 'sched2026',    'clearance': 'ORANGE'},
}

CONTEXT_DIR = Path(__file__).parent / 'context'


def authenticate_group(group_id: str, password: str):
    """Return group dict if credentials valid, else None."""
    group = GROUPS.get(group_id)
    if group and group['password'] == password:
        return group
    return None


def load_group_context(group_id: str) -> str:
    """Load group context from markdown file. Raises FileNotFoundError if missing."""
    context_file = CONTEXT_DIR / f'{group_id}_context.md'
    if not context_file.exists():
        raise FileNotFoundError(
            f'No context file for {group_id}. '
            f'Create context/{group_id}_context.md first.'
        )
    return context_file.read_text()
