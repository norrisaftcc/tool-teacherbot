"""Skin registry and auth helpers.

A "skin" is a URL-prefixed cohort surface. Each skin ships its own
passcode, model, display copy, cohort header, and (optional) vendored
corpus directory. Routes are mounted at ``/<slug>/…`` per skin.
"""
from __future__ import annotations

from pathlib import Path
from typing import TypedDict

CONTEXT_DIR = Path(__file__).parent / 'context'


class Skin(TypedDict):
    password: str
    model: str
    clearance: str          # kept for DB Group.clearance_level compat
    display: str
    tagline: str
    header_file: str        # relative to context/
    corpus_dir: str | None  # relative to context/, or None if no corpus vendored


SKINS: dict[str, Skin] = {
    'csc114': {
        'password': '2026su',
        'model': 'claude-sonnet-4-6',
        'clearance': 'ORANGE',
        'display': 'CSC 114 — Fundamentals of AI/ML',
        'tagline': 'Summer 2026 pilot.',
        'header_file': 'csc114_context.md',
        'corpus_dir': 'csc114',
    },
    'csc134': {
        'password': 'csc134-tbd',
        'model': 'claude-haiku-4-5-20251001',
        'clearance': 'ORANGE',
        'display': 'CSC 134 — Introduction to Programming',
        'tagline': 'Fall 2026 cohort.',
        'header_file': 'csc134_context.md',
        'corpus_dir': 'csc134',
    },
}


def authenticate_skin(slug: str, password: str) -> Skin | None:
    """Return the skin entry if credentials valid, else None."""
    skin = SKINS.get(slug)
    if skin and skin['password'] == password:
        return skin
    return None


def load_skin_context(slug: str) -> str:
    """Load a skin's cohort header, appending the vendored corpus if any.

    Raises FileNotFoundError if the header file is missing.
    """
    skin = SKINS.get(slug)
    if skin is None:
        raise KeyError(f'unknown skin: {slug!r}')

    header_path = CONTEXT_DIR / skin['header_file']
    if not header_path.exists():
        raise FileNotFoundError(
            f'Cohort header missing for {slug}: expected {header_path}.'
        )
    text = header_path.read_text()

    corpus_dir_name = skin.get('corpus_dir')
    if corpus_dir_name:
        corpus_dir = CONTEXT_DIR / corpus_dir_name
        if corpus_dir.is_dir():
            corpus_chunks: list[str] = []
            for corpus_file in sorted(corpus_dir.rglob('*.md')):
                rel = corpus_file.relative_to(corpus_dir)
                corpus_chunks.append(f'\n\n--- corpus: {rel} ---\n\n{corpus_file.read_text()}')
            if corpus_chunks:
                text += ''.join(corpus_chunks)
    return text


# --------------------------------------------------------------------------
# Backward-compat aliases — kept so pre-refactor tests and any lingering
# route callers still import successfully across T5 → T7. Deleted in T8.
# --------------------------------------------------------------------------

_LEGACY_GROUPS: dict[str, dict[str, str]] = {
    'group2': {'password': 'dataman2026', 'clearance': 'YELLOW'},
    'group3': {'password': 'finaid2026',  'clearance': 'ORANGE'},
    'group4': {'password': 'health2026',  'clearance': 'YELLOW'},
    'group5': {'password': 'sched2026',   'clearance': 'ORANGE'},
}

# GROUPS keeps its pre-refactor keyset ({csc114, group2..5}) so pre-T7 tests
# see no drift. csc134 is deliberately excluded: it is a new-contract skin
# and callers should reach it via SKINS. This dict is deleted in T8.
GROUPS: dict[str, dict[str, str]] = {
    'csc114': {'password': SKINS['csc114']['password'], 'clearance': SKINS['csc114']['clearance']},
    **_LEGACY_GROUPS,
}


def authenticate_group(group_id: str, password: str) -> dict | None:
    """Deprecated alias — use ``authenticate_skin``."""
    group = GROUPS.get(group_id)
    if group and group['password'] == password:
        return group
    return None


def load_group_context(group_id: str) -> str:
    """Deprecated alias — use ``load_skin_context``.

    For legacy ``group{N}`` ids that never became skins, falls back to
    reading ``context/{group_id}_context.md`` verbatim.
    """
    if group_id in SKINS:
        return load_skin_context(group_id)
    context_file = CONTEXT_DIR / f'{group_id}_context.md'
    if not context_file.exists():
        raise FileNotFoundError(
            f'No context file for {group_id}. '
            f'Create context/{group_id}_context.md before students log in.'
        )
    return context_file.read_text()
