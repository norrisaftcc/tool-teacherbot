"""Skin registry and auth helpers.

A "skin" is a URL-prefixed cohort surface. Each skin ships its own
passcode, model, persona, display copy, cohort header, and (optional)
vendored corpus directory. Routes are mounted at ``/<slug>/…`` per skin.

Per ADR-0002 the corpus is *windowed*: only the small always-on index
files plus one active module reach the system prompt. The rest stays
vendored on disk and out of the prompt.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TypedDict

CONTEXT_DIR = Path(__file__).parent / 'context'


class Skin(TypedDict):
    password: str
    model: str
    clearance: str            # kept for DB Group.clearance_level compat
    display: str
    tagline: str
    persona_file: str         # relative to context/
    header_file: str          # relative to context/
    corpus_dir: str | None    # relative to context/, or None if no corpus vendored
    corpus_index: list[str]   # always-on paths under corpus_dir (file or dir)
    active_module: str | None  # the one subdirectory of corpus_dir to load


SKINS: dict[str, Skin] = {
    'csc114': {
        'password': '2026su',
        'model': 'claude-sonnet-4-6',
        'clearance': 'ORANGE',
        'display': 'CSC 114 — Fundamentals of AI/ML',
        'tagline': 'Summer 2026 pilot.',
        'persona_file': 'csc114_persona.md',
        'header_file': 'csc114_context.md',
        'corpus_dir': 'csc114',
        'corpus_index': ['crosswalk.md'],
        'active_module': 'week-02-keras-hello-world',
    },
    'csc134': {
        'password': 'csc134-tbd',
        'model': 'claude-haiku-4-5-20251001',
        'clearance': 'ORANGE',
        'display': 'CSC 134 — Introduction to Programming',
        'tagline': 'Fall 2026 cohort.',
        'persona_file': 'csc134_persona.md',
        'header_file': 'csc134_context.md',
        'corpus_dir': 'csc134',
        'corpus_index': ['outline'],
        'active_module': 'modules/m0',
    },
}


def active_module(slug: str) -> str | None:
    """The module window for a skin, honouring a ``<SLUG>_ACTIVE_MODULE``
    env override so a course lead can advance the week from the Render
    dashboard instead of shipping a commit.

    An override naming a directory that does not exist is ignored (and
    logged) rather than silently emptying the bot's context — a typo in
    a dashboard field must not blank the corpus.
    """
    skin = SKINS[slug]
    override = (os.getenv(f'{slug.upper()}_ACTIVE_MODULE') or '').strip()
    if not override:
        return skin['active_module']

    corpus_dir_name = skin.get('corpus_dir')
    if corpus_dir_name:
        resolved = _resolve_within(CONTEXT_DIR / corpus_dir_name, override)
        if resolved is not None and resolved.is_dir():
            return override

    logging.getLogger(__name__).warning(
        '%s_ACTIVE_MODULE=%r does not resolve to a directory under '
        'context/%s — falling back to %r.',
        slug.upper(), override, corpus_dir_name, skin['active_module'],
    )
    return skin['active_module']


def authenticate_skin(slug: str, password: str) -> Skin | None:
    """Return the skin entry if credentials valid, else None."""
    skin = SKINS.get(slug)
    if skin and skin['password'] == password:
        return skin
    return None


def _resolve_within(root: Path, rel: str) -> Path | None:
    """Resolve ``rel`` under ``root``, refusing anything that escapes it.

    Symlinks are not followed — a hostile symlink at context/<slug>/x.md
    pointed at /etc/passwd would otherwise flow into Claude's system
    prompt and out to a student. Returns None if the path is missing,
    is a symlink, or resolves outside ``root``.
    """
    if not root.is_dir() or root.is_symlink():
        return None
    candidate = root / rel
    if not candidate.exists() or candidate.is_symlink():
        return None
    try:
        resolved = candidate.resolve()
        resolved.relative_to(root.resolve())
    except (OSError, ValueError):
        return None
    return candidate


def _corpus_chunks(corpus_dir: Path, target: Path) -> list[str]:
    """Render every safe .md file at or under ``target`` as a labelled chunk."""
    if target.is_file():
        files = [target] if target.suffix == '.md' else []
    else:
        files = sorted(target.rglob('*.md'))

    chunks: list[str] = []
    for corpus_file in files:
        rel = corpus_file.relative_to(corpus_dir)
        if _resolve_within(corpus_dir, str(rel)) is None or not corpus_file.is_file():
            continue
        # Explicit utf-8: the corpus is markdown vendored from GitHub, and
        # read_text()'s default is the *platform* encoding — cp1252 on
        # Windows, ascii under LANG=C. Either one raises on the first
        # curly quote or em dash in the course material.
        body = corpus_file.read_text(encoding='utf-8')
        chunks.append(f'\n\n--- corpus: {rel.as_posix()} ---\n\n{body}')
    return chunks


def load_skin_persona(slug: str) -> str:
    """Load a skin's persona — who the assistant is and how it behaves.

    Raises FileNotFoundError if the persona file is missing.
    """
    skin = SKINS.get(slug)
    if skin is None:
        raise KeyError(f'unknown skin: {slug!r}')

    persona_path = CONTEXT_DIR / skin['persona_file']
    if not persona_path.exists():
        raise FileNotFoundError(
            f'Persona missing for {slug}: expected {persona_path}.'
        )
    return persona_path.read_text(encoding='utf-8')


def load_skin_context(slug: str) -> str:
    """Load a skin's cohort header plus its *windowed* corpus.

    The window is the always-on ``corpus_index`` entries followed by the
    single ``active_module`` directory. Everything else in the corpus
    stays on disk and out of the prompt — see ADR-0002.

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
    text = header_path.read_text(encoding='utf-8')

    corpus_dir_name = skin.get('corpus_dir')
    if not corpus_dir_name:
        return text
    corpus_dir = CONTEXT_DIR / corpus_dir_name

    window = list(skin.get('corpus_index') or [])
    module = active_module(slug)
    if module:
        window.append(module)

    chunks: list[str] = []
    for entry in window:
        target = _resolve_within(corpus_dir, entry)
        if target is None:
            logging.getLogger(__name__).warning(
                'Corpus entry %r missing for skin %s (looked under %s).',
                entry, slug, corpus_dir,
            )
            continue
        chunks.extend(_corpus_chunks(corpus_dir, target))

    return text + ''.join(chunks)


