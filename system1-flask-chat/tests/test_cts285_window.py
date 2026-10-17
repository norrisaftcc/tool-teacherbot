"""Window guards for the cts285 skin: size, stability, and what may be in it.

Every guard here asserts on the ASSEMBLED prompt: the text
``claude_handler._system_blocks`` builds, which is the block that is cached
and sent. It is composed from the real header, persona, teaching notes and
vendored corpus on disk. A guard scoped to the file that was edited passes its
own revert and still misses the defect (``algorithm-shodann`` EARLY_RUNS 18
took three attempts for that reason).

Three decisions are encoded here and are not mine to relax:

* **The cache floor stays at 4096 estimated tokens** (bytes / 4), as the user
  asked. In-repo notes say Haiku 5.5 will cache at 512, which this session
  could not verify. Every window clears 4096 by a wide margin, and bytes / 4
  under-counts Haiku 5.5 tokens, which is the conservative direction for a
  floor. ``test_auth.py`` guards csc134 against the same floor and composes
  *without* teaching notes. This file composes WITH them, through
  ``_system_blocks``, because that is where the cached block is built.
* **A missing corpus fails. It does not skip.** A guard that skips when the
  thing is absent passes in exactly the situation it exists for.
* **Parametrize lists are asserted non-empty and exact**, because an empty
  ``parametrize`` is a silent pass.

The upstream course repository is private and is not read here.
"""
import importlib.util
import json
import re
import shutil
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

import auth
import claude_handler

APP_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = APP_DIR.parent
CONTEXT = APP_DIR / 'context'
CORPUS = CONTEXT / 'cts285'
MODULES_DIR = CORPUS / 'modules'

EXPECTED_MODULES = [f'm{n}' for n in range(9)]
FLOOR_TOKENS = 4096          # the user's decision: keep the conservative floor
CEILING_TOKENS = 60_000      # margin under the 100k rate-card threshold
HAIKU_5_5_TOKEN_FACTOR = 1.3  # ~30% more tokens than Haiku 4.5 for the same text

# Found on disk, not listed: a window added or lost changes the parametrize.
# ``test_the_windows_are_exactly_m0_to_m8`` fails if the discovery is wrong.
WINDOWS = sorted(p.name for p in MODULES_DIR.iterdir() if p.is_dir()) \
    if MODULES_DIR.is_dir() else []


# ---- helpers ---------------------------------------------------------------

def _compose(module: str | None = None, monkeypatch=None) -> str:
    """The cached system block's text, built the way the chat route builds it.

    ``module`` sets ``CTS285_ACTIVE_MODULE`` through monkeypatch, so it is
    restored on teardown. None composes whatever the environment says.
    """
    if module is not None:
        monkeypatch.setenv('CTS285_ACTIVE_MODULE', module)
    block = claude_handler._system_blocks(
        auth.load_skin_context('cts285'),
        auth.load_skin_persona('cts285'),
        auth.load_skin_notes('cts285'),
    )[0]
    assert block['type'] == 'text'
    return block['text']


def _estimated_tokens(text: str) -> int:
    """bytes / 4, the estimate test_auth.py uses for the csc134 floor."""
    return len(text.encode('utf-8')) // 4


def _real_token_estimate(text: str) -> float:
    return len(text.encode('utf-8')) * HAIKU_5_5_TOKEN_FACTOR / 4


def _floor_failure(text: str) -> str | None:
    """None when the window clears the floor, otherwise the reason."""
    tokens = _estimated_tokens(text)
    if tokens < FLOOR_TOKENS:
        return f'{tokens} estimated tokens is under the {FLOOR_TOKENS} cache floor'
    return None


def _ceiling_failure(text: str) -> str | None:
    tokens = _real_token_estimate(text)
    if tokens >= CEILING_TOKENS:
        return f'{tokens:.0f} estimated Haiku 5.5 tokens is over {CEILING_TOKENS}'
    return None


def _tripwires():
    """The A2 content tripwires, read from the corpus test rather than copied.

    Both suites are packages named ``tests``, so the root suite's module is
    loaded by path. Copying the list would let the two drift, and the drift
    would loosen this guard silently.
    """
    path = REPO_ROOT / 'tests' / 'test_cts285_corpus.py'
    assert path.is_file(), f'{path} is missing; the tripwires have no source'
    spec = importlib.util.spec_from_file_location('cts285_corpus_tripwires', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    patterns = module.FORBIDDEN_CONTENT
    assert len(patterns) >= 10, patterns
    return patterns


def _vendored_text() -> str:
    files = [p for p in CORPUS.rglob('*.md') if p.is_file()]
    assert files, 'no vendored markdown to search'
    return '\n'.join(p.read_text(encoding='utf-8') for p in files)


# ---- the discovery guards --------------------------------------------------

def test_the_windows_are_exactly_m0_to_m8():
    """Exact, not merely non-empty. A missing window would otherwise just be
    one fewer parametrized case and nothing red."""
    assert WINDOWS == EXPECTED_MODULES, WINDOWS


def test_the_corpus_and_the_always_on_index_exist():
    # assert, never skip
    assert CORPUS.is_dir(), f'{CORPUS} is missing'
    manual = CORPUS / 'reference' / '18-the-dataman-manual.md'
    assert manual.is_file(), f'{manual} is missing'
    assert 'two tries' in manual.read_text(encoding='utf-8')


def test_the_skin_window_resolves_for_every_module(monkeypatch):
    """The module selector and the files agree. If ``active_module`` quietly
    fell back to the default, every parametrized case below would be testing
    m4 under nine names."""
    assert WINDOWS
    for module in WINDOWS:
        monkeypatch.setenv('CTS285_ACTIVE_MODULE', module)
        assert auth.active_module('cts285') == module
        assert auth.module_window('cts285') == [f'modules/{module}']
        assert f'--- corpus: modules/{module}/' in auth.load_skin_context('cts285')


# ---- size ------------------------------------------------------------------

@pytest.mark.parametrize('module', WINDOWS)
def test_window_clears_the_cache_floor(module, monkeypatch):
    text = _compose(module, monkeypatch)
    assert _floor_failure(text) is None, f'{module}: {_floor_failure(text)}'


@pytest.mark.parametrize('module', WINDOWS)
def test_window_stays_under_the_rate_card_ceiling(module, monkeypatch):
    text = _compose(module, monkeypatch)
    assert _ceiling_failure(text) is None, f'{module}: {_ceiling_failure(text)}'


def _tiny_context(tmp_path: Path, module: str = 'm2', body: str = 'tiny.') -> Path:
    """A context dir with the real header, persona and notes and a corpus of
    one short page per window. Used to prove the size guards fail."""
    for name in ('cts285_context.md', 'cts285_persona.md', 'cts285_teaching_notes.md'):
        shutil.copy(CONTEXT / name, tmp_path / name)
    for rel in ('reference/18-the-dataman-manual.md', f'modules/{module}/page.md'):
        target = tmp_path / 'cts285' / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding='utf-8')
    return tmp_path


def test_the_floor_guard_fails_when_the_window_is_shrunk(tmp_path, monkeypatch):
    """The guard has teeth. With a one-line corpus the same helper the real
    windows pass through must report a failure, using the real header,
    persona and notes."""
    monkeypatch.setattr(auth, 'CONTEXT_DIR', _tiny_context(tmp_path))
    monkeypatch.setenv('CTS285_ACTIVE_MODULE', 'm2')
    text = _compose()
    assert 'corpus: modules/m2/page.md' in text, 'the shrunken corpus was not composed'
    failure = _floor_failure(text)
    assert failure is not None and 'cache floor' in failure, failure


def test_the_ceiling_guard_fails_when_the_window_is_inflated(tmp_path, monkeypatch):
    body = 'This sentence stands in for course text. ' * 7000   # ~280 KB
    monkeypatch.setattr(auth, 'CONTEXT_DIR', _tiny_context(tmp_path, body=body))
    monkeypatch.setenv('CTS285_ACTIVE_MODULE', 'm2')
    failure = _ceiling_failure(_compose())
    assert failure is not None and 'over' in failure, failure


def test_the_floor_guard_fails_when_the_corpus_is_absent(tmp_path, monkeypatch):
    """A missing corpus must fail, not skip. The loader only logs a warning
    for it, so the guard is the thing that notices."""
    for name in ('cts285_context.md', 'cts285_persona.md', 'cts285_teaching_notes.md'):
        shutil.copy(CONTEXT / name, tmp_path / name)
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    monkeypatch.setenv('CTS285_ACTIVE_MODULE', 'm2')
    assert _floor_failure(_compose()) is not None


# ---- stability and content -------------------------------------------------

@pytest.mark.parametrize('module', WINDOWS)
def test_window_is_byte_identical_across_env_override_round_trips(module, monkeypatch):
    """Switch to another module and back. Nothing about the previous
    composition may stay in the block: no counter, no cache of the old
    window, no ordering that depends on directory iteration state."""
    first = _compose(module, monkeypatch)
    other = 'm0' if module != 'm0' else 'm1'
    elsewhere = _compose(other, monkeypatch)
    assert elsewhere != first
    again = _compose(module, monkeypatch)
    assert again.encode('utf-8') == first.encode('utf-8')


@pytest.mark.parametrize('module', WINDOWS)
def test_window_says_two_tries(module, monkeypatch):
    assert 'two tries' in _compose(module, monkeypatch)


@pytest.mark.parametrize('module', WINDOWS)
def test_window_contains_no_answer_key_or_instructor_tripwire(module, monkeypatch):
    text = _compose(module, monkeypatch)
    patterns = _tripwires()
    hits = [p.pattern for p in patterns if p.search(text)]
    assert not hits, f'{module}: assembled prompt matches {hits}'


def test_the_block_carries_the_one_hour_cache_marker(monkeypatch):
    block = claude_handler._system_blocks(
        auth.load_skin_context('cts285'), auth.load_skin_persona('cts285'),
        auth.load_skin_notes('cts285'))
    assert len(block) == 1
    assert block[0]['cache_control'] == {'type': 'ephemeral', 'ttl': '1h'}


# ---- persona, notes and header ---------------------------------------------

# A3's forbidden strings. "clearance" is allowed only in the sentence that
# tells the bot it has none.
_FORBIDDEN_IN_VOICE_FILES = [
    re.compile(r'AlgoCratic', re.I),
    re.compile(r'The Algorithm', re.I),
    re.compile(r'SHODANN', re.I),
    re.compile(r'DataMan Corp', re.I),
    re.compile(r'\bCLO\b'),                      # CLO 1..5, "CLOs", "CLO-3"
    re.compile(r'learning outcome\s*(?:no\.?|number|#)?\s*\d', re.I),
]
_CLEARANCE_OK = re.compile(r'\bno\s+clearance\b', re.I)
_VOICE_FILES = ('cts285_persona.md', 'cts285_teaching_notes.md', 'cts285_context.md')


@pytest.mark.parametrize('name', _VOICE_FILES)
def test_voice_files_carry_no_forbidden_string(name):
    text = (CONTEXT / name).read_text(encoding='utf-8')
    assert text.strip(), f'{name} is empty'
    hits = [p.pattern for p in _FORBIDDEN_IN_VOICE_FILES if p.search(text)]
    assert not hits, f'{name} matches {hits}'
    # "clearance" only inside "no clearance". Strip the allowed phrase, then
    # no other use may remain.
    leftover = _CLEARANCE_OK.sub('', text)
    assert not re.search(r'clearance', leftover, re.I), (
        f'{name} uses "clearance" outside the sentence that says the tutor has none')


def test_persona_still_tells_the_tutor_it_holds_no_clearance():
    """The other half of the exception above. Remove the sentence and the
    exemption has nothing to exempt."""
    text = (CONTEXT / 'cts285_persona.md').read_text(encoding='utf-8')
    assert _CLEARANCE_OK.search(text)


def test_voice_files_carry_no_time_varying_content():
    """The header must be byte-stable: no dates, times or counters."""
    date = re.compile(r'\b(?:19|20)\d{2}-\d{2}-\d{2}\b|\b\d{1,2}:\d{2}\b'
                      r'|\b(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day\b')
    for name in _VOICE_FILES:
        text = (CONTEXT / name).read_text(encoding='utf-8')
        assert not date.search(text), f'{name}: {date.search(text).group(0)!r}'


_DOCS_PATH = re.compile(r'`?(docs/[A-Za-z0-9_<>./-]+?\.md)`?(?![A-Za-z0-9_<>/-])')


def test_every_artifact_path_in_persona_and_notes_appears_in_a_vendored_page():
    """A path that no page shows is a path a student cannot be held to.
    The register in the notes was copied from the governance file, and only
    paths that a vendored page asks for belong in it."""
    named = set()
    for name in ('cts285_persona.md', 'cts285_teaching_notes.md'):
        named.update(_DOCS_PATH.findall((CONTEXT / name).read_text(encoding='utf-8')))
    assert len(named) >= 20, f'only {len(named)} artifact paths found: {sorted(named)}'
    vendored = _vendored_text()
    missing = sorted(p for p in named if p not in vendored)
    assert not missing, f'named in persona/notes, shown on no vendored page: {missing}'


def test_the_path_checker_actually_catches_a_path_no_page_shows():
    """The check above would also pass if ``_DOCS_PATH`` matched nothing
    useful. Prove it finds a path in text and that the search can miss."""
    found = _DOCS_PATH.findall('Put it at `docs/definitely-not-a-page.md` please.')
    assert found == ['docs/definitely-not-a-page.md']
    assert 'docs/definitely-not-a-page.md' not in _vendored_text()


# ---- byte stability through the Flask client -------------------------------

def _text_block(text):
    return SimpleNamespace(type='text', text=text)


def _response():
    usage = SimpleNamespace(input_tokens=1, output_tokens=1,
                            cache_creation_input_tokens=0, cache_read_input_tokens=0)
    return SimpleNamespace(content=[_text_block('ok')], usage=usage, stop_reason='end_turn')


def _login(client):
    return client.post('/cts285/login', data={'username': 'CTS285', 'password': 'algorithm'})


def _history(prefix, n):
    return [{'role': 'user' if i % 2 == 0 else 'assistant', 'content': f'{prefix}-{i}'}
            for i in range(n)]


def test_system_argument_is_identical_across_seats(app):
    """Two logins, two different histories and messages, one ``system``.

    Nothing guarded this before (CLAUDE.md, Prompt composition). A per-seat
    byte in the cached block gives every seat its own cache entry, and 1h
    writes bill at about 2x against reads at about 0.1x. The token counter
    cannot see it, because cache reads count at full weight in
    ``_usage_total``. Only the invoice moves.
    """
    mock = MagicMock()
    mock.messages.create.return_value = _response()
    seen = []
    with patch('claude_handler.client', mock):
        for prefix, n, message in (('alpha', 2, 'What is a requirement?'),
                                   ('bravo', 7, 'How do I cite the manual?')):
            seat = app.test_client()       # a new cookie jar is a new seat
            assert _login(seat).status_code == 302
            r = seat.post('/cts285/api/chat',
                          json={'message': message, 'history': _history(prefix, n)})
            assert r.status_code == 200
            kwargs = mock.messages.create.call_args.kwargs
            assert kwargs['messages'][-1]['content'] == message
            seen.append(kwargs['system'])
    assert len(seen) == 2
    assert seen[0] == seen[1]
    assert json.dumps(seen[0], sort_keys=True) == json.dumps(seen[1], sort_keys=True)
    # And the block is the real window, not an empty stand-in.
    assert _floor_failure(seen[0][0]['text']) is None


def test_system_argument_is_identical_on_the_stream_path(app):
    def stream_client():
        client = MagicMock()
        fake = MagicMock()
        fake.text_stream = iter(['a', 'b'])
        fake.get_final_message.return_value = _response()
        client.messages.stream.return_value.__enter__.return_value = fake
        client.messages.stream.return_value.__exit__.return_value = False
        return client

    systems = []
    for prefix, n, message in (('alpha', 0, 'first'), ('bravo', 5, 'second')):
        client = stream_client()
        with patch('claude_handler.client', client):
            seat = app.test_client()
            assert _login(seat).status_code == 302
            r = seat.post('/cts285/api/chat/stream',
                          json={'message': message, 'history': _history(prefix, n)})
            assert r.status_code == 200
            r.get_data()                   # drain the generator so the call is made
            systems.append(client.messages.stream.call_args.kwargs['system'])
    assert systems[0] == systems[1]
    assert _floor_failure(systems[0][0]['text']) is None


def test_system_argument_does_not_carry_the_seat_or_the_history(app):
    """Positive control for the test above: if the block held the message or
    the history, the equality would already have failed, but name the bytes
    that must not be there."""
    mock = MagicMock()
    mock.messages.create.return_value = _response()
    with patch('claude_handler.client', mock):
        seat = app.test_client()
        _login(seat)
        seat.post('/cts285/api/chat',
                  json={'message': 'UNIQUE-QUESTION-9f3a', 'history': _history('UNIQUE-HIST-7c1d', 3)})
    text = mock.messages.create.call_args.kwargs['system'][0]['text']
    assert 'UNIQUE-QUESTION-9f3a' not in text
    assert 'UNIQUE-HIST-7c1d' not in text
