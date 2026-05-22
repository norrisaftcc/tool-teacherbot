import logging
import re
from pathlib import Path

log = logging.getLogger(__name__)

# Alpha: hardcoded credentials. Replace with DB-backed auth post-alpha.
GROUPS = {
    'csc114': {'password': '2026su',     'clearance': 'ORANGE'},
    'group2': {'password': 'dataman2026', 'clearance': 'YELLOW'},
    'group3': {'password': 'finaid2026',  'clearance': 'ORANGE'},
    'group4': {'password': 'health2026',  'clearance': 'YELLOW'},
    'group5': {'password': 'sched2026',   'clearance': 'ORANGE'},
}

CONTEXT_DIR = Path(__file__).parent / 'context'


def authenticate_group(group_id: str, password: str) -> dict | None:
    """Return group dict if credentials valid, else None."""
    group = GROUPS.get(group_id)
    if group and group['password'] == password:
        return group
    return None


def _corpus_label(group_id: str) -> str:
    """Turn 'csc114' → 'CSC 114', 'group2' → 'GROUP 2' for corpus headers."""
    return re.sub(r'([A-Za-z]+)(\d+)', r'\1 \2', group_id).upper()


def load_group_context(group_id: str) -> str:
    """Load group context for `group_id`.

    Reads `context/{group_id}_context.md` (required). If
    `context/{group_id}/` is also a directory, every `.md` file beneath it
    is appended in sorted relative-path order, each prefixed with a header
    naming the path. Non-.md files are skipped with a warning.
    """
    context_file = CONTEXT_DIR / f'{group_id}_context.md'
    if not context_file.exists():
        raise FileNotFoundError(
            f'No context file for {group_id}. '
            f'Create context/{group_id}_context.md before students log in.'
        )

    parts = [context_file.read_text()]

    corpus_dir = CONTEXT_DIR / group_id
    if corpus_dir.is_dir():
        md_files = sorted(
            (p for p in corpus_dir.rglob('*') if p.is_file()),
            key=lambda p: p.relative_to(corpus_dir).as_posix(),
        )
        if md_files:
            parts.append(f'\n=== {_corpus_label(group_id)} CORPUS ===\n')
        for f in md_files:
            rel = f.relative_to(corpus_dir).as_posix()
            if f.suffix.lower() != '.md':
                log.warning('skipping non-markdown corpus file: %s', rel)
                continue
            parts.append(f'\n## {rel}\n')
            parts.append(f.read_text())

    return ''.join(parts)
