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
    active_module: str | None  # the module *id* currently in the window
    module_paths: list[str]   # '{module}' templates expanded per active_module


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
        'module_paths': ['{module}'],
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
        'active_module': 'm0',
        # Upstream splits one week across two trees: modules/mN is what the
        # module is *about* (overview, objectives, readings), assignments/mN
        # is what the student is actually doing. A window with only the first
        # answers "what are this week's outcomes" and not "how do I open my
        # Codespace" — see the ADR-0002 amendment.
        'module_paths': ['modules/{module}', 'assignments/{module}'],
    },
}


def module_window(slug: str) -> list[str]:
    """Corpus-relative paths for the active module, in prompt order.

    Expands each ``module_paths`` template with the active module id, so a
    course lead advances the week by setting one short value (``m3``)
    rather than editing a list of paths.
    """
    skin = SKINS[slug]
    module = active_module(slug)
    if not module:
        return []
    templates = skin.get('module_paths') or ['{module}']
    return [template.format(module=module) for template in templates]


def _module_resolves(slug: str, module: str) -> bool:
    """True if at least one of this skin's module paths exists for `module`."""
    skin = SKINS[slug]
    corpus_dir_name = skin.get('corpus_dir')
    if not corpus_dir_name:
        return False
    corpus_dir = CONTEXT_DIR / corpus_dir_name
    templates = skin.get('module_paths') or ['{module}']
    for template in templates:
        resolved = _resolve_within(corpus_dir, template.format(module=module))
        if resolved is not None and resolved.is_dir():
            return True
    return False


def active_module(slug: str) -> str | None:
    """The active module id for a skin, honouring a ``<SLUG>_ACTIVE_MODULE``
    env override so a course lead can advance the week from the Render
    dashboard instead of shipping a commit.

    An override that resolves to nothing is ignored (and logged) rather
    than silently emptying the bot's context — a typo in a dashboard field
    must not blank the corpus. "Resolves" means *at least one* of the
    skin's module paths exists: csc134's assignments/mN is authored a
    module at a time, so a module with a reading but no assignment yet is
    a normal, valid state.
    """
    skin = SKINS[slug]
    override = (os.getenv(f'{slug.upper()}_ACTIVE_MODULE') or '').strip()
    if not override:
        return skin['active_module']

    if _module_resolves(slug, override):
        return override

    logging.getLogger(__name__).warning(
        '%s_ACTIVE_MODULE=%r resolves to no corpus path under context/%s '
        '— falling back to %r.',
        slug.upper(), override, skin.get('corpus_dir'), skin['active_module'],
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

    The window is the always-on ``corpus_index`` entries followed by every
    path the active module expands to. Everything else in the corpus stays
    on disk and out of the prompt — see ADR-0002 and its amendment.

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

    log = logging.getLogger(__name__)
    chunks: list[str] = []

    # Index entries are configuration: one missing is a misconfigured skin.
    for entry in skin.get('corpus_index') or []:
        target = _resolve_within(corpus_dir, entry)
        if target is None:
            log.warning(
                'Corpus index entry %r missing for skin %s (looked under %s).',
                entry, slug, corpus_dir,
            )
            continue
        chunks.extend(_corpus_chunks(corpus_dir, target))

    # Module paths are content: a module with a reading but no assignment
    # yet is normal while a course is being authored, so an individually
    # missing path is not worth waking anyone at 2am. All of them missing
    # means the active module isn't vendored at all — that is worth saying.
    module_entries = module_window(slug)
    found_any = False
    for entry in module_entries:
        target = _resolve_within(corpus_dir, entry)
        if target is None:
            log.debug('Module path %r not vendored for skin %s.', entry, slug)
            continue
        found_any = True
        chunks.extend(_corpus_chunks(corpus_dir, target))

    if module_entries and not found_any:
        log.warning(
            'Active module %r for skin %s resolves to none of %s — the '
            'prompt will carry the cohort header and index only.',
            active_module(slug), slug, module_entries,
        )

    return text + ''.join(chunks)


