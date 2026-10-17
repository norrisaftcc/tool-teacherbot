"""Sync a course corpus from an upstream repo into a vendored target.

Reads the manifest at --manifest (default: scripts/csc114_manifest.yaml
for back-compat), clones the upstream repo into a temp directory, copies
listed paths into the manifest's target, and removes anything in the
target that the new copy did not produce.

Run from the repo root:
    python scripts/sync_course_corpus.py                                # csc114
    python scripts/sync_course_corpus.py --manifest scripts/csc134_manifest.yaml
    python scripts/sync_course_corpus.py --manifest scripts/cts285_manifest.yaml \\
        --source /path/to/a/local/clone                                  # private upstream

Optional manifest keys, all absent from the csc114/csc134 manifests so those
two keep their exact old behaviour:

  map:         ordered [{from: prefix, to: prefix}] rewrites of the destination
               path (after strip_prefix). First match wins; component-aware.
  transforms:  {'.html': 'html-to-markdown', '.py': 'fence', ...}. The output
               is a .md file, so the corpus loader (which reads *.md) sees it.
  deny:        a hard guard, separate from `exclude`. Where `exclude` silently
               skips a file, `deny` RAISES and writes nothing, because a
               denied path in `paths` means the allow-list itself is wrong.
"""
from __future__ import annotations

import argparse
import fnmatch
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


def load_manifest(path: Path) -> dict[str, Any]:
    # Explicit utf-8: read_text() defaults to the *platform* encoding, so on
    # Windows a substitution containing an em dash round-trips through
    # cp1252 and lands in the corpus as mojibake ("â€”"). Observed, fixed.
    return yaml.safe_load(path.read_text(encoding='utf-8'))


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


# ---------------------------------------------------------------------------
# deny: the hard guard
# ---------------------------------------------------------------------------

def _posix(rel: str | Path) -> str:
    """Normalise an upstream-relative path to a clean POSIX string.

    `..` is refused outright. A `module-02/../planning/x` entry would pass a
    component check for `planning/` only if it were collapsed first, and a
    guard that can be walked around by punctuation is not a guard.
    """
    text = str(rel).replace('\\', '/')
    if text.startswith('/') or '..' in PurePosixPath(text).parts:
        raise ValueError(f'manifest path must be relative and may not contain "..": {rel}')
    return posixpath.normpath(text)


def deny_match(rel: str, patterns: list[str], is_dir: bool = False) -> str | None:
    """Return the first `deny` pattern that matches `rel`, else None.

    `rel` is the upstream-relative POSIX path. Deliberately NOT
    `PurePath.match('**')`: on Python 3.11 `**` is not recursive there, so a
    pattern written as `**/build-guides/**` would look like it worked and
    match only one level. Two plain rules instead, both case-sensitive
    (`fnmatchcase`, so Windows and Linux agree):

    * a pattern ending `/` names a directory. It matches when that name (or a
      run of names, for `a/b/`) appears as a path component at any depth.
      For a file only the parent components count; for a listed directory
      every component counts.
    * any other pattern is matched against the filename and against the
      whole path.
    """
    parts = rel.split('/')
    dir_parts = parts if is_dir else parts[:-1]
    name = parts[-1]
    for pat in patterns:
        if pat.endswith('/'):
            want = pat.rstrip('/').split('/')
            n = len(want)
            for start in range(len(dir_parts) - n + 1):
                window = dir_parts[start:start + n]
                if all(fnmatch.fnmatchcase(c, w) for c, w in zip(window, want)):
                    return pat
        elif fnmatch.fnmatchcase(name, pat) or fnmatch.fnmatchcase(rel, pat):
            return pat
    return None


def _check_denied(rel: str, patterns: list[str], is_dir: bool = False) -> None:
    hit = deny_match(rel, patterns, is_dir)
    if hit is not None:
        raise ValueError(f'denied path in manifest: {rel} (matches deny pattern {hit!r})')


# ---------------------------------------------------------------------------
# map: destination prefix rewrites
# ---------------------------------------------------------------------------

def apply_map(dest: str, rules: list[dict[str, str]]) -> str:
    """Rewrite the destination path with the first matching `map` rule.

    A rule matches on a whole path component: `from: module-02/` matches
    `module-02/a.html` and never `module-02x/a.html`. `from` may also be one
    exact file path, which is how a single page is lifted out of its module
    folder.
    """
    for rule in rules:
        src = _posix(rule['from'])
        to = (rule.get('to') or '').replace('\\', '/')
        if dest == src or dest.startswith(src + '/'):
            remainder = dest[len(src):]
            joined = to.rstrip('/') + remainder
            return joined.lstrip('/')
    return dest


# ---------------------------------------------------------------------------
# transforms
# ---------------------------------------------------------------------------

_FENCE_LANG = {
    '.py': 'python', '.txt': 'text', '.html': 'html', '.js': 'javascript',
    '.css': 'css', '.json': 'json', '.yaml': 'yaml', '.yml': 'yaml',
    '.sh': 'bash', '.sql': 'sql', '.toml': 'toml', '.ini': 'ini',
}
_TRANSFORMS = ('html-to-markdown', 'fence')


def _fence(text: str, lang: str) -> str:
    """Wrap `text` in a code fence longer than any backtick run inside it."""
    longest = max((len(m.group(0)) for m in re.finditer(r'`+', text)), default=0)
    ticks = '`' * max(3, longest + 1)
    return f'{ticks}{lang}\n{text.rstrip(chr(10))}\n{ticks}\n'


def fence_text(text: str, suffix: str) -> str:
    return _fence(text, _FENCE_LANG.get(suffix.lower(), 'text'))


class _MarkdownParser(HTMLParser):
    """Canvas page body -> plain Markdown, standard library only.

    The vendored corpus is read by a language model, not rendered, so the aim
    is legible structure and no styling noise, not round-trip fidelity.
    Inline `style=` and every other attribute are never read.
    """

    _SKIP = {'script', 'style'}
    _PARA = {'p'}
    _LINE = {'div', 'section', 'br', 'tr', 'hr', 'blockquote', 'article', 'header', 'footer'}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.blocks: list[str] = []      # <pre> bodies, restored after whitespace collapse
        self.caps: list[list[str]] = []  # capture stack (headings, cells, links, ...)
        self.kinds: list[tuple] = []     # what each capture is for
        self.skip = 0
        self.pre: list[str] | None = None
        self.lists: list[list] = []      # [tag, counter]
        self.li_depth = 0
        self.row: list[str] | None = None

    # -- output plumbing ---------------------------------------------------
    def _emit(self, text: str) -> None:
        (self.caps[-1] if self.caps else self.out).append(text)

    def _push(self, kind: tuple) -> None:
        self.caps.append([])
        self.kinds.append(kind)

    def _pop(self) -> tuple[tuple, str]:
        kind = self.kinds.pop()
        text = re.sub(r'\s+', ' ', ''.join(self.caps.pop())).strip()
        return kind, text

    def _close_kind(self, name: str) -> tuple[tuple, str] | None:
        """Pop the innermost capture of `name`, closing any unclosed ones above it."""
        if not any(k[0] == name for k in self.kinds):
            return None
        while True:
            kind, text = self._pop()
            if kind[0] == name:
                return kind, text
            self._emit(text)

    # -- parser callbacks --------------------------------------------------
    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in self._SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        if self.pre is not None:
            return                       # markup inside <pre> is plain text
        a = dict(attrs)
        if tag == 'pre':
            self.pre = []
        elif re.fullmatch(r'h[1-6]', tag):
            self._emit('\n\n')
            self._push(('h', '#' * int(tag[1])))
        elif tag in self._PARA:
            self._emit(' ' if self._in_li() else '\n\n')
        elif tag in ('ul', 'ol'):
            self.lists.append([tag, 0])
            self._emit('\n')
        elif tag == 'li':
            depth = max(len(self.lists) - 1, 0)
            if self.lists and self.lists[-1][0] == 'ol':
                self.lists[-1][1] += 1
                bullet = f'{self.lists[-1][1]}. '
            else:
                bullet = '- '
            self.li_depth += 1
            self._emit('\n' + '\x01' * (2 * depth) + bullet)
        elif tag == 'div' and self._in_li():
            self._emit(' ')
        elif tag in self._LINE:
            self._emit('\n')
        elif tag == 'details':
            self._emit('\n')
        elif tag == 'summary':
            self._emit('\n')
            self._push(('summary',))
        elif tag in ('strong', 'b'):
            self._push(('mark', '**'))
        elif tag in ('em', 'i'):
            self._push(('mark', '*'))
        elif tag == 'code':
            self._push(('code',))
        elif tag == 'a':
            self._push(('a', a.get('href') or ''))
        elif tag == 'img':
            alt = (a.get('alt') or '').strip()
            if alt:
                self._emit(f'[Image: {alt}]')
        elif tag == 'table':
            self._emit('\n')
        elif tag == 'tr':
            self._flush_row()
            self.row = []
            self._emit('\n')
        elif tag in ('td', 'th'):
            if self.row is None:
                self.row = []
            self._push(('cell',))

    def handle_startendtag(self, tag: str, attrs: list) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in ('br', 'img', 'hr'):
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP:
            self.skip = max(self.skip - 1, 0)
            return
        if self.skip:
            return
        if self.pre is not None:
            if tag == 'pre':
                body = ''.join(self.pre).strip('\n')
                self.pre = None
                self.blocks.append(_fence(body, ''))
                self._emit(f'\n\n\x00{len(self.blocks) - 1}\x00\n\n')
            return
        if re.fullmatch(r'h[1-6]', tag):
            got = self._close_kind('h')
            if got:
                kind, text = got
                self._emit(f'{kind[1]} {text}\n\n' if text else '\n')
        elif tag in self._PARA:
            self._emit('' if self._in_li() else '\n\n')
        elif tag in ('ul', 'ol'):
            if self.lists:
                self.lists.pop()
            self._emit('\n')
        elif tag == 'li':
            self.li_depth = max(self.li_depth - 1, 0)
        elif tag in ('div', 'section', 'details', 'blockquote'):
            self._emit('\n')
        elif tag == 'summary':
            got = self._close_kind('summary')
            if got:
                self._emit(f'**{got[1]}**\n' if got[1] else '')
        elif tag in ('strong', 'b', 'em', 'i'):
            got = self._close_kind('mark')
            if got:
                kind, text = got
                self._emit(f'{kind[1]}{text}{kind[1]}' if text else '')
        elif tag == 'code':
            got = self._close_kind('code')
            if got:
                self._emit(f'`{got[1]}`' if got[1] else '')
        elif tag == 'a':
            got = self._close_kind('a')
            if got:
                kind, text = got
                href = kind[1].strip()
                linkable = (re.match(r'https?://', href, re.I) is not None
                            and 'LINK-PENDING' not in href)
                self._emit(f'[{text}]({href})' if (text and linkable) else text)
        elif tag in ('td', 'th'):
            got = self._close_kind('cell')
            if got and self.row is not None:
                self.row.append(got[1])
        elif tag == 'tr':
            self._flush_row()
        elif tag == 'table':
            self._flush_row()
            self._emit('\n')

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        if self.pre is not None:
            self.pre.append(data)
            return
        data = data.replace('\x00', '').replace('\x01', '').replace('\xa0', ' ')
        self._emit(re.sub(r'\s+', ' ', data))

    def _in_li(self) -> bool:
        return self.li_depth > 0

    def _flush_row(self) -> None:
        # Unclosed cells would otherwise leak their capture into the row.
        while self.kinds and self.kinds[-1][0] == 'cell':
            _, text = self._pop()
            if self.row is not None:
                self.row.append(text)
        if self.row:
            self._emit(' | '.join(self.row))
        self.row = None
        self._emit('\n')

    # -- result ------------------------------------------------------------
    def result(self) -> str:
        while self.caps:
            _, text = self._pop()
            self.out.append(text)
        if self.pre is not None:         # unterminated <pre>
            self.blocks.append(_fence(''.join(self.pre).strip('\n'), ''))
            self.out.append(f'\n\n\x00{len(self.blocks) - 1}\x00\n\n')
        lines = []
        for raw in ''.join(self.out).split('\n'):
            indent = len(raw) - len(raw.lstrip('\x01'))
            body = re.sub(r' {2,}', ' ', raw.lstrip('\x01')).strip()
            lines.append(' ' * indent + body if body else '')
        text = '\n'.join(lines)
        text = re.sub(r'\n{3,}', '\n\n', text).strip('\n')
        text = re.sub(r'\x00(\d+)\x00', lambda m: self.blocks[int(m.group(1))].rstrip('\n'), text)
        return text + '\n' if text else ''


def html_to_markdown(source: str) -> str:
    """Convert a Canvas HTML page body to Markdown (stdlib `html.parser` only)."""
    parser = _MarkdownParser()
    parser.feed(source)
    parser.close()
    return parser.result()


def apply_transform(mode: str, text: str, suffix: str) -> str:
    if mode == 'html-to-markdown':
        return html_to_markdown(text)
    if mode == 'fence':
        return fence_text(text, suffix)
    raise ValueError(f'unknown transform {mode!r} (expected one of {_TRANSFORMS})')


def _transformed_name(dest_rel: PurePosixPath, mode: str) -> PurePosixPath:
    """`page.html` -> `page.md`; fenced `app.py` -> `app.py.md`."""
    if mode == 'html-to-markdown':
        return dest_rel.with_suffix('.md')
    return dest_rel.with_name(dest_rel.name + '.md')


# ---------------------------------------------------------------------------
# local source
# ---------------------------------------------------------------------------

def _git(source: Path, *args: str) -> str:
    done = subprocess.run(['git', '-C', str(source), *args],
                          capture_output=True, text=True)
    if done.returncode != 0:
        raise ValueError(f'git {" ".join(args[:2])} failed in {source}: {done.stderr.strip()}')
    return done.stdout


def local_source_sha(source: Path, paths: list[str]) -> str:
    """Return the HEAD SHA of a local checkout, or raise.

    The corpus records which commit it came from. A checkout with uncommitted
    changes under a manifest path would make that SHA a lie, so it is refused
    rather than warned about. Untracked files count as changes: porcelain
    lists them.
    """
    source = Path(source).resolve()
    if not source.is_dir():
        raise ValueError(f'--source is not a directory: {source}')
    try:
        top = Path(_git(source, 'rev-parse', '--show-toplevel').strip()).resolve()
    except (ValueError, FileNotFoundError) as exc:
        raise ValueError(f'--source is not a git repository: {source} ({exc})') from exc
    if top != source:
        raise ValueError(f'--source must be the root of a git repository, not inside one: '
                         f'{source} is inside {top}')
    sha = _git(source, 'rev-parse', 'HEAD').strip()
    dirty = _git(source, 'status', '--porcelain', '--', *paths).strip()
    if dirty:
        raise ValueError(f'--source has uncommitted changes under manifest paths:\n{dirty}')
    return sha


# ---------------------------------------------------------------------------
# apply
# ---------------------------------------------------------------------------

def _plan(manifest: dict[str, Any], fetched_root: Path) -> tuple[list[tuple[Path, PurePosixPath, str | None]], int]:
    """Resolve every manifest entry to (source, destination-relative, transform).

    Everything that can raise does so here, before a single byte is written.
    That is what lets `deny` promise "nothing is written": the guard and the
    copy are two phases, not one loop.
    """
    strip_prefix = manifest.get('strip_prefix', '') or ''
    prefix_path = Path(strip_prefix) if strip_prefix else None
    exclude = list(manifest.get('exclude') or [])
    deny = list(manifest.get('deny') or [])
    rules = list(manifest.get('map') or [])
    transforms = {k.lower(): v for k, v in (manifest.get('transforms') or {}).items()}
    for mode in transforms.values():
        if mode not in _TRANSFORMS:
            raise ValueError(f'unknown transform {mode!r} (expected one of {_TRANSFORMS})')

    plan: list[tuple[Path, PurePosixPath, str | None]] = []
    excluded = 0
    seen: dict[PurePosixPath, Path] = {}

    def add(file_src: Path, upstream_rel: Path) -> None:
        rel_path = upstream_rel
        if prefix_path and rel_path.is_relative_to(prefix_path):
            dest = rel_path.relative_to(prefix_path).as_posix()
        else:
            dest = rel_path.as_posix()
        dest_rel = PurePosixPath(apply_map(dest, rules))
        mode = transforms.get(file_src.suffix.lower())
        if mode:
            dest_rel = _transformed_name(dest_rel, mode)
        if dest_rel.is_absolute() or '..' in dest_rel.parts:
            raise ValueError(f'mapped destination escapes the target: {dest_rel}')
        if dest_rel in seen and seen[dest_rel] != file_src:
            raise ValueError(f'two sources map to one destination {dest_rel}: '
                             f'{seen[dest_rel]} and {file_src}')
        seen[dest_rel] = file_src
        plan.append((file_src, dest_rel, mode))

    for rel in manifest['paths']:
        src = fetched_root / rel
        if src.is_symlink():
            raise ValueError(f'manifest path is a symlink (refusing to follow): {rel}')
        if not src.exists():
            raise FileNotFoundError(f'manifest path not in upstream: {rel}')

        if deny:
            _check_denied(_posix(rel), deny, is_dir=src.is_dir())
        rel_path = Path(rel)
        if is_excluded(rel_path, exclude):
            excluded += 1
            continue

        if src.is_dir():
            for child in sorted(src.rglob('*')):
                if child.is_symlink() or not child.is_file():
                    continue
                child_rel = child.relative_to(fetched_root)
                if deny:
                    _check_denied(_posix(child_rel.as_posix()), deny)
                if is_excluded(child_rel, exclude):
                    excluded += 1
                    continue
                add(child, rel_path / child.relative_to(src))
        else:
            add(src, rel_path)
    return plan, excluded


def apply_manifest(
    manifest: dict[str, Any],
    fetched_root: Path,
    target: Path,
    provenance: dict[str, str] | None = None,
) -> dict[str, int]:
    """Copy manifest paths from `fetched_root` into `target`, deleting stragglers.

    Returns a small summary dict:
    {'files': N, 'bytes': M, 'excluded': K, 'rewrites': R}, plus
    'transformed': T when at least one transform ran.

    `provenance`, when given, is written to `<target>/_provenance.txt` as
    `key: value` lines. It is `.txt`, so the corpus loader never reads it, and
    it is excluded from the summary counts.
    """
    subs = compile_substitutions(manifest.get('substitutions') or [])
    plan, excluded_count = _plan(manifest, fetched_root)
    rewrite_count = 0
    transformed_count = 0
    written: set[Path] = set()

    target.mkdir(parents=True, exist_ok=True)
    target_resolved = target.resolve()
    for src, dest_rel, mode in plan:
        out = target / Path(*dest_rel.parts)
        if not out.resolve().is_relative_to(target_resolved):
            raise ValueError(f'destination escapes the target: {dest_rel}')
        out.parent.mkdir(parents=True, exist_ok=True)
        if mode:
            text = src.read_text(encoding='utf-8')
            out.write_text(apply_transform(mode, text, src.suffix), encoding='utf-8')
            transformed_count += 1
        else:
            shutil.copy2(src, out)
        written.add(out.resolve())

    # Rewrite vendored markdown. Done here rather than at load time so the
    # corpus on disk is exactly what the bot sees — a reviewer reading
    # context/ should not have to mentally apply a regex to know what
    # reaches the prompt. Transformed pages are .md by now, so they are
    # rewritten too.
    if subs:
        for path in sorted(written):
            if path.suffix != '.md':
                continue
            original = path.read_text(encoding='utf-8')
            rewritten, n = apply_substitutions(original, subs)
            if n:
                path.write_text(rewritten, encoding='utf-8')
                rewrite_count += n

    total_bytes = sum(p.stat().st_size for p in written)
    file_count = len(written)

    keep = set(written)
    if provenance:
        prov = target / '_provenance.txt'
        prov.write_text(''.join(f'{k}: {v}\n' for k, v in provenance.items()), encoding='utf-8')
        keep.add(prov.resolve())

    # Delete anything in target that we didn't just write.
    for existing in list(target.rglob('*')):
        if existing.is_file() and existing.resolve() not in keep:
            existing.unlink()
    # Prune now-empty directories.
    for d in sorted(target.rglob('*'), key=lambda p: -len(p.parts)):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()

    summary = {
        'files': file_count,
        'bytes': total_bytes,
        'excluded': excluded_count,
        'rewrites': rewrite_count,
    }
    if transformed_count:
        # Only present when a transform ran, so a manifest without
        # `transforms` returns exactly the dict it always did.
        summary['transformed'] = transformed_count
    return summary


_NEW_KEYS = ('map', 'transforms', 'deny')


def main(argv: list[str] | None = None) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description='Sync a course corpus into the vendored target.')
    parser.add_argument(
        '--manifest',
        default=str(repo_root / 'scripts' / 'csc114_manifest.yaml'),
        help='Path to the manifest YAML (default: scripts/csc114_manifest.yaml).',
    )
    parser.add_argument(
        '--source',
        default=None,
        help='Use this local git checkout instead of cloning the manifest upstream. '
             'Required in practice for a private upstream. Must be clean under every '
             'manifest path.',
    )
    args = parser.parse_args(argv)
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = (Path.cwd() / manifest_path).resolve()
    manifest = load_manifest(manifest_path)

    target = repo_root / manifest['target']
    modern = args.source is not None or any(manifest.get(k) for k in _NEW_KEYS)

    def run(fetched: Path, sha: str | None) -> dict[str, int]:
        prov = None
        if modern and sha:
            try:
                shown = manifest_path.relative_to(repo_root).as_posix()
            except ValueError:
                shown = manifest_path.name
            prov = {'source_sha': sha, 'upstream': manifest['upstream'], 'manifest': shown}
        return apply_manifest(manifest, fetched, target, provenance=prov)

    if args.source is not None:
        source = Path(args.source)
        sha = local_source_sha(source, [str(p) for p in manifest['paths']])
        summary = run(source.resolve(), sha)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            fetched = Path(tmp) / 'upstream'
            fetch_upstream(manifest['upstream'], manifest['ref'], fetched)
            sha = None
            if modern:
                try:
                    sha = _git(fetched, 'rev-parse', 'HEAD').strip()
                except ValueError:
                    sha = None
            summary = run(fetched, sha)

    est_tokens = summary['bytes'] // 4
    extra = f", {summary['transformed']} converted" if summary.get('transformed') else ''
    print(f"sync complete: {summary['files']} files, {summary['bytes']} bytes "
          f"(~{est_tokens} tokens vendored on disk); "
          f"{summary['excluded']} excluded, {summary['rewrites']} link(s) rewritten{extra}")
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
