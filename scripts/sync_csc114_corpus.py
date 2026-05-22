"""Sync the CSC 114 corpus from an upstream repo into a vendored target.

Reads scripts/csc114_manifest.yaml, clones the upstream repo into a temp
directory, copies listed paths into the target, and removes anything in
the target that the new copy did not produce.

Run from the repo root:
    python scripts/sync_csc114_corpus.py
"""
from __future__ import annotations

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


def apply_manifest(manifest: dict[str, Any], fetched_root: Path, target: Path) -> dict[str, int]:
    """Copy manifest paths from `fetched_root` into `target`, deleting stragglers.

    Returns a small summary dict: {'files': N, 'bytes': M}.
    """
    strip_prefix = manifest.get('strip_prefix', '') or ''
    prefix_path = Path(strip_prefix) if strip_prefix else None
    written: set[Path] = set()

    for rel in manifest['paths']:
        src = fetched_root / rel
        if src.is_symlink():
            raise ValueError(f'manifest path is a symlink (refusing to follow): {rel}')
        if not src.exists():
            raise FileNotFoundError(f'manifest path not in upstream: {rel}')

        rel_path = Path(rel)
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
                    out = dest / child.relative_to(src)
                    out.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(child, out)
                    written.add(out.resolve())
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            written.add(dest.resolve())

    # Delete anything in target that we didn't just write.
    for existing in list(target.rglob('*')):
        if existing.is_file() and existing.resolve() not in written:
            existing.unlink()
    # Prune now-empty directories.
    for d in sorted(target.rglob('*'), key=lambda p: -len(p.parts)):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()

    total_bytes = sum(p.stat().st_size for p in written)
    return {'files': len(written), 'bytes': total_bytes}


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    manifest_path = repo_root / 'scripts' / 'csc114_manifest.yaml'
    manifest = load_manifest(manifest_path)

    target = repo_root / manifest['target']
    target.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        fetched = Path(tmp) / 'upstream'
        fetch_upstream(manifest['upstream'], manifest['ref'], fetched)
        summary = apply_manifest(manifest, fetched, target)

    est_tokens = summary['bytes'] // 4
    print(f"sync complete: {summary['files']} files, {summary['bytes']} bytes "
          f"(~{est_tokens} tokens)")
    if est_tokens > 30_000:
        print('WARNING: corpus exceeds ~30k token soft budget. '
              'Review before merging.', file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
