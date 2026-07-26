import os
from collections.abc import Generator
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

MODEL = 'claude-sonnet-4-6'
MAX_TOKENS = 1024

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

    Returns:
        (response_text, total_tokens_used)
    """
    messages = history + [{'role': 'user', 'content': user_message}]

    try:
        response = client.messages.create(
            model=model or MODEL,
            max_tokens=MAX_TOKENS,
            system=_system_blocks(group_context, persona, notes),
            messages=messages,
        )
    except Exception as e:
        raise RuntimeError(f'Claude API error: {e}') from e

    text = response.content[0].text
    return text, _usage_total(response.usage)


def stream_claude_response(
    group_context: str,
    history: list[dict],
    user_message: str,
    model: str | None = None,
    persona: str | None = None,
    notes: str | None = None,
) -> Generator[tuple[str, int], None, None]:
    """
    Stream Claude response token by token.

    Yields (text_chunk, 0) for each text delta, then ('' , total_tokens) once at the end.
    Raises RuntimeError on API failure.
    """
    messages = history + [{'role': 'user', 'content': user_message}]

    try:
        with client.messages.stream(
            model=model or MODEL,
            max_tokens=MAX_TOKENS,
            system=_system_blocks(group_context, persona, notes),
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield text, 0
            final = stream.get_final_message()
            yield '', _usage_total(final.usage)
    except Exception as e:
        raise RuntimeError(f'Claude API error: {e}') from e
