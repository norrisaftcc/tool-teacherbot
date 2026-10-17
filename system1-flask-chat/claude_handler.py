import logging
import os
from collections.abc import Generator
from anthropic import Anthropic

logger = logging.getLogger(__name__)

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# One client per per-skin key. Keyed on (env var name, key value) so that
# rotating the key in the dashboard takes effect on the next request without
# a stale client holding the old one. The module-level `client` above is
# still the default and the seam the tests patch.
_skin_clients: dict[tuple[str, str], Anthropic] = {}

# Env var names already warned about, so a blank per-skin key logs once per
# process and not once per student message.
_warned_blank_key_envs: set[str] = set()


def _client_for(api_key_env: str | None):
    """The client for a skin: its own key if ``api_key_env`` names a set
    variable, otherwise the module-level ``client``.

    Falling back to the global client when the variable is unset is
    deliberate. A skin that declares a key variable nobody has set yet should
    still answer, on the shared credits, rather than 502 every student.
    The module-level ``client`` is looked up at call time so a test patching
    ``claude_handler.client`` still intercepts every call.
    """
    if not api_key_env:
        return client
    key = (os.getenv(api_key_env) or '').strip()
    if not key:
        # Deliberate fallback (see above), but a silent one: a skin meant to
        # bill its own key would spend the shared one and nothing would say so.
        if api_key_env not in _warned_blank_key_envs:
            _warned_blank_key_envs.add(api_key_env)
            logger.warning(
                'api_key_env %s is unset or blank; falling back to the shared '
                'Anthropic key for this skin.', api_key_env)
        return client
    cache_key = (api_key_env, key)
    if cache_key not in _skin_clients:
        _skin_clients[cache_key] = Anthropic(api_key=key)
    return _skin_clients[cache_key]


# What a student sees when the model declines (stop_reason == 'refusal').
# Without it the stream path ends with no text and the page shows an empty
# bubble, which reads as a crash. Out of character on purpose.
REFUSAL_TEXT = "I can't help with that one. Ask your instructor."

# What a student sees when the model spends the whole output ceiling and
# produces no text (stop_reason == 'max_tokens'). Haiku 5.5 thinks by default
# and thinking counts against max_tokens, so a response can end inside the
# thinking block. Without a line the page shows an empty bubble. A partial
# answer that did reach the student is left alone, not overwritten.
MAX_TOKENS_TEXT = 'That answer ran too long. Ask a narrower question.'

_RESERVED_KWARGS = frozenset({'model', 'max_tokens', 'system', 'messages', 'stream'})


def _request_kwargs(model, max_tokens, request_options, system, messages) -> dict:
    """The kwargs for messages.create/stream.

    With no ``request_options`` and no ``max_tokens`` this is exactly the
    call the module has always made. ``request_options`` is merged on top;
    a key that collides with one the handler owns is a configuration bug and
    raises rather than silently winning.
    """
    kwargs = {
        'model': model or MODEL,
        'max_tokens': max_tokens or MAX_TOKENS,
        'system': system,
        'messages': messages,
    }
    if request_options:
        clash = _RESERVED_KWARGS & set(request_options)
        if clash:
            raise ValueError(
                f'request_options may not set {sorted(clash)}; the handler owns them.'
            )
        kwargs.update(request_options)
    return kwargs


def _response_text(response) -> str:
    """Join the text blocks of a response.

    Taking ``content[0].text`` assumed the first block is text. On a model
    that thinks by default, the first block can be a ``thinking`` block,
    which has no ``.text`` — an AttributeError, or an empty answer.
    """
    return ''.join(
        block.text for block in (response.content or [])
        if getattr(block, 'type', None) == 'text'
    )

MODEL = 'claude-sonnet-4-6'
# 1024 truncated a real answer mid-word: eval sample 5's m0-07 ended "What
# *does* compile and run w". That item runs long because it correctly shows a
# broken snippet and then explains why the compiler blames the *next* line —
# which is the kind of answer this bot exists to give.
#
# Output is small next to the ~7.2k cached prefix every message already
# carries, and the cohort budget is 25M, so the cost of the extra headroom is
# noise. `truncated-at-max-tokens` in the eval harness now catches a recurrence
# instead of leaving it to whoever reads the transcript.
MAX_TOKENS = 2048

# Fallback persona for callers that don't pass one. Routes always pass a
# per-skin persona from context/<slug>_persona.md (ADR-0002); this is a
# course-agnostic safety net, deliberately carrying the pedagogical
# guardrails and none of the cohort flavour.
DEFAULT_PERSONA = """You are an AI teaching assistant for a college course.

PEDAGOGICAL RULES:
1. Never provide direct solutions — guide students through iteration
2. Ask students to explain their attempt before you help
3. Ask clarifying questions before answering
4. Reference the course materials below when relevant
5. Celebrate iteration and learning velocity, not just correct answers

RESPONSE STYLE:
- Technical but encouraging
- Concise; prefer a short concrete answer to a sweeping survey
"""


def build_system_prompt(course_context: str, persona: str | None = None,
                        notes: str | None = None) -> str:
    """Compose the system prompt: who the assistant is, how this course
    teaches, then what it knows.

    The three parts are kept distinct because they change on different
    clocks — the persona is voice and rarely moves, the notes are
    course-wide pedagogy, and the context is windowed per module.
    """
    teaching = f'\nHOW THIS COURSE TEACHES:\n{notes}\n' if notes else ''
    return f"""{persona or DEFAULT_PERSONA}
{teaching}
COURSE CONTEXT:
{course_context}
"""


_USAGE_FIELDS = (
    'input_tokens',
    'cache_creation_input_tokens',
    'cache_read_input_tokens',
    'output_tokens',
)


def _usage_total(usage) -> int:
    """Total billable tokens, cache included.

    Once the system prompt is cached, the corpus stops showing up in
    ``input_tokens`` and moves to the cache counters — summing only
    input+output would under-report a cohort's budget by the size of
    the whole module window. The cache fields are typed Optional by the
    SDK, so skip anything that isn't an int.
    """
    return sum(
        value for value in (getattr(usage, f, 0) for f in _USAGE_FIELDS)
        if isinstance(value, int)
    )


def _system_blocks(course_context: str, persona: str | None,
                   notes: str | None = None) -> list[dict]:
    """The system prompt as a single cached block.

    The whole prompt is byte-stable for a given (skin, active module), so
    every student in a cohort shares one cache entry — the second and
    later messages in a class period bill it at ~10% of input price.
    The 1h TTL (2x write, vs 1.25x at the 5m default) is sized for a
    class period: it pays back from the third read.
    """
    return [{
        'type': 'text',
        'text': build_system_prompt(course_context, persona, notes),
        'cache_control': {'type': 'ephemeral', 'ttl': '1h'},
    }]


def get_claude_response(
    group_context: str,
    history: list[dict],
    user_message: str,
    model: str | None = None,
    persona: str | None = None,
    notes: str | None = None,
    max_tokens: int | None = None,
    request_options: dict | None = None,
    api_key_env: str | None = None,
) -> tuple[str, int]:
    """
    Call Claude with context and conversation history.

    Args:
        group_context: The cohort header + windowed corpus markdown string
        history: List of {'role': 'user'|'assistant', 'content': str} dicts
        user_message: The new message from the student
        model: Anthropic model id; defaults to module-level MODEL when omitted.
        persona: Per-skin persona markdown; defaults to DEFAULT_PERSONA.
        notes: Per-skin course-wide teaching notes; omitted when empty.
        max_tokens: Per-skin output ceiling; defaults to MAX_TOKENS.
        request_options: Extra kwargs for the API call (e.g. output_config).
        api_key_env: Env var naming a per-skin API key; unset uses the shared one.

    Returns:
        (response_text, total_tokens_used)
    """
    text, tokens, _ = get_claude_response_full(
        group_context, history, user_message,
        model=model, persona=persona, notes=notes,
        max_tokens=max_tokens, request_options=request_options,
        api_key_env=api_key_env,
    )
    return text, tokens


def get_claude_response_full(
    group_context: str,
    history: list[dict],
    user_message: str,
    model: str | None = None,
    persona: str | None = None,
    notes: str | None = None,
    max_tokens: int | None = None,
    request_options: dict | None = None,
    api_key_env: str | None = None,
) -> tuple[str, int, str | None]:
    """As get_claude_response, plus the API's ``stop_reason``.

    Split out rather than widening get_claude_response, whose two-value
    shape the routes and their tests depend on. The eval harness wants the
    stop reason so it can flag an answer cut off at max_tokens — a defect
    that is invisible to every other check, and was found by reading a
    transcript rather than by any flag (sample 5's m0-07 ended mid-word).

    The alternative was guessing truncation from the text, which flagged a
    bullet list that simply ended without punctuation. An exact signal
    exists; approximating it would have been a flag that cries wolf, and K3
    is the rule that makes that expensive.
    """
    messages = history + [{'role': 'user', 'content': user_message}]

    kwargs = _request_kwargs(
        model, max_tokens, request_options,
        _system_blocks(group_context, persona, notes), messages,
    )
    try:
        response = _client_for(api_key_env).messages.create(**kwargs)
    except Exception as e:
        raise RuntimeError(f'Claude API error: {e}') from e

    stop_reason = getattr(response, 'stop_reason', None)
    if stop_reason == 'refusal':
        text = REFUSAL_TEXT
    else:
        text = _response_text(response)
        if stop_reason == 'max_tokens' and not text.strip():
            text = MAX_TOKENS_TEXT
    return text, _usage_total(response.usage), stop_reason


def stream_claude_response(
    group_context: str,
    history: list[dict],
    user_message: str,
    model: str | None = None,
    persona: str | None = None,
    notes: str | None = None,
    max_tokens: int | None = None,
    request_options: dict | None = None,
    api_key_env: str | None = None,
) -> Generator[tuple[str, int], None, None]:
    """
    Stream Claude response token by token.

    Yields (text_chunk, 0) for each text delta, then ('' , total_tokens) once at the end.
    A refusal yields REFUSAL_TEXT as a final text chunk before the totals.
    A max_tokens stop with no text streamed yields MAX_TOKENS_TEXT the same way.
    Raises RuntimeError on API failure.
    """
    messages = history + [{'role': 'user', 'content': user_message}]
    kwargs = _request_kwargs(
        model, max_tokens, request_options,
        _system_blocks(group_context, persona, notes), messages,
    )

    try:
        with _client_for(api_key_env).messages.stream(**kwargs) as stream:
            emitted = False
            for text in stream.text_stream:
                emitted = emitted or bool(text)
                yield text, 0
            final = stream.get_final_message()
            stop_reason = getattr(final, 'stop_reason', None)
            if stop_reason == 'refusal':
                # Separate from any partial answer already on screen.
                yield ('\n\n' if emitted else '') + REFUSAL_TEXT, 0
            elif stop_reason == 'max_tokens' and not emitted:
                yield MAX_TOKENS_TEXT, 0
            yield '', _usage_total(final.usage)
    except Exception as e:
        raise RuntimeError(f'Claude API error: {e}') from e
