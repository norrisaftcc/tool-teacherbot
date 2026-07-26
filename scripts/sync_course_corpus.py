"""Sync a course corpus from an upstream repo into a vendored target.

Reads the manifest at --manifest (default: scripts/csc114_manifest.yaml
for back-compat), clones the upstream repo into a temp directory, copies
listed paths into the manifest's target, and removes anything in the
target that the new copy did not produce.

Run from the repo root:
    python scripts/sync_course_corpus.py                                # csc114
    python scripts/sync_course_corpus.py --manifest scripts/csc134_manifest.yaml
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml


def load_manifest(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text())


def fetch_upstream(url: str, ref: str, dest: Path) -> None:
    """Shallow-clone `url` at `ref` into `dest`. Raises on failure."""
    subprocess.run(
        ['git', 'clone', '--depth', '1', '--branch', ref, url, str(dest)],
        check=True,
    )


def is_excluded(rel: Path, patterns: list[str]) -> bool:
    """True if `rel` (relative to the upstream root) matches any exclude glob.

    Exists because a course repo mixes student- and instructor-facing files
    in the same directory — an answer key sitting next to the reading it
    answers. Vendoring one into a student-facing bot puts it in the system
    prompt, where no amount of persona wording reliably keeps it back.
    """
    return any(rel.match(pattern) for pattern in patterns)


def compile_substitutions(raw: list[dict[str, str]]) -> list[tuple[re.Pattern, str]]:
    """Compile manifest `substitutions` into (pattern, replacement) pairs."""
    return [(re.compile(entry['pattern']), entry.get('replace', '')) for entry in raw]


def apply_substitutions(text: str, subs: list[tuple[re.Pattern, str]]) -> tuple[str, int]:
    """Rewrite `text`, returning the result and how many edits were made.

    Vendoring takes a *subset* of a repo whose documents assume the whole
    repo, so cross-references can point at files that exist upstream and
    not here. A student following one finds nothing, and the bot will
    happily repeat it — that behaviour was observed, not theorised.
    """
    total = 0
    for pattern, replacement in subs:
        text, n = pattern.subn(replacement, text)
        total += n
    return text, total


def apply_manifest(manifest: dict[str, Any], fetched_root: Path, target: Path) -> dict[str, int]:
    """Copy manifest paths from `fetched_root` into `target`, deleting stragglers.

    Returns a small summary dict:
    {'files': N, 'bytes': M, 'excluded': K, 'rewrites': R}.
    """
    strip_prefix = manifest.get('strip_prefix', '') or ''
    prefix_path = Path(strip_prefix) if strip_prefix else None
    exclude = list(manifest.get('exclude') or [])
    subs = compile_substitutions(manifest.get('substitutions') or [])
    excluded_count = 0
    rewrite_count = 0
    written: set[Path] = set()

    for rel in manifest['paths']:
        src = fetched_root / rel
        if src.is_symlink():
            raise ValueError(f'manifest path is a symlink (refusing to follow): {rel}')
        if not src.exists():
            raise FileNotFoundError(f'manifest path not in upstream: {rel}')

        rel_path = Path(rel)
        if is_excluded(rel_path, exclude):
            excluded_count += 1
            continue
        if prefix_path and rel_path.is_relative_to(prefix_path):
            dest_rel = rel_path.relative_to(prefix_path)
        else:
            dest_rel = rel_path
        dest = target / dest_rel

        if src.is_dir():
            for child in src.rglob('*'):
                if child.is_symlink():
                    continue
                if child.is_file():
                    if is_excluded(child.relative_to(fetched_root), exclude):
                        excluded_count += 1
                        continue
                    out = dest / child.relative_to(src)
                    out.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(child, out)
                    written.add(out.resolve())
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            written.add(dest.resolve())

    # Rewrite vendored markdown. Done here rather than at load time so the
    # corpus on disk is exactly what the bot sees — a reviewer reading
    # context/ should not have to mentally apply a regex to know what
    # reaches the prompt.
    if subs:
        for path in sorted(written):
            if path.suffix != '.md':
                continue
            original = path.read_text(encoding='utf-8')
            rewritten, n = apply_substitutions(original, subs)
            if n:
                path.write_text(rewritten, encoding='utf-8')
                rewrite_count += n

    # Delete anything in target that we didn't just write.
    for existing in list(target.rglob('*')):
        if existing.is_file() and existing.resolve() not in written:
            existing.unlink()
    # Prune now-empty directories.
    for d in sorted(target.rglob('*'), key=lambda p: -len(p.parts)):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()

    total_bytes = sum(p.stat().st_size for p in written)
    return {
        'files': len(written),
        'bytes': total_bytes,
        'excluded': excluded_count,
        'rewrites': rewrite_count,
    }


def main(argv: list[str] | None = None) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description='Sync a course corpus into the vendored target.')
    parser.add_argument(
        '--manifest',
        default=str(repo_root / 'scripts' / 'csc114_manifest.yaml'),
        help='Path to the manifest YAML (default: scripts/csc114_manifest.yaml).',
    )
    args = parser.parse_args(argv)
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = (Path.cwd() / manifest_path).resolve()
    manifest = load_manifest(manifest_path)

    target = repo_root / manifest['target']
    target.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        fetched = Path(tmp) / 'upstream'
        fetch_upstream(manifest['upstream'], manifest['ref'], fetched)
        summary = apply_manifest(manifest, fetched, target)

    est_tokens = summary['bytes'] // 4
    print(f"sync complete: {summary['files']} files, {summary['bytes']} bytes "
          f"(~{est_tokens} tokens vendored on disk); "
          f"{summary['excluded']} excluded, {summary['rewrites']} link(s) rewritten")
    if est_tokens > 30_000:
        # Not necessarily a problem since ADR-0002: only `corpus_index`
        # plus one `active_module` reaches the system prompt. Worth a look
        # anyway — a single module this large would blow the window.
        print('NOTE: vendored corpus exceeds ~30k tokens. Only the active '
              'window reaches the prompt; check that no single module is '
              'oversized.', file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
