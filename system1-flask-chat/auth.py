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


