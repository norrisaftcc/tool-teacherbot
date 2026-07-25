# tests/test_claude_handler.py
from unittest.mock import MagicMock, patch
import claude_handler
from claude_handler import (
    DEFAULT_PERSONA,
    build_system_prompt,
    get_claude_response,
    stream_claude_response,
)

SAMPLE_CONTEXT = """
# CSC 114 — cohort header
## Course
- Product: DataMan Math Platform
- Tech Stack: Flask, SQLite, React
"""

SAMPLE_PERSONA = "You are a teaching assistant for CSC 134, an intro C++ course."


def test_system_prompt_contains_context():
    prompt = build_system_prompt(SAMPLE_CONTEXT)
    assert 'DataMan' in prompt


def test_system_prompt_uses_supplied_persona():
    prompt = build_system_prompt(SAMPLE_CONTEXT, persona=SAMPLE_PERSONA)
    assert SAMPLE_PERSONA in prompt
    assert 'DataMan' in prompt
    # The supplied persona replaces the fallback rather than stacking on it —
    # two personas in one prompt is worse than either alone.
    assert DEFAULT_PERSONA not in prompt


def test_system_prompt_falls_back_to_default_persona():
    prompt = build_system_prompt(SAMPLE_CONTEXT)
    assert DEFAULT_PERSONA in prompt


def test_default_persona_keeps_guardrails_without_cohort_flavour():
    """The fallback is course-agnostic: guardrails yes, AlgoCratic no."""
    assert 'direct solution' in DEFAULT_PERSONA.lower()
    assert 'AlgoCratic' not in DEFAULT_PERSONA
    assert 'The Algorithm' not in DEFAULT_PERSONA


def test_get_claude_response_returns_text_and_tokens():
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text='Test response')]
    mock_message.usage.input_tokens = 100
    mock_message.usage.output_tokens = 50
    mock_client.messages.create.return_value = mock_message

    with patch('claude_handler.client', mock_client):
        response, tokens = get_claude_response(SAMPLE_CONTEXT, [], 'Hello')
        assert response == 'Test response'
        assert tokens == 150


def test_get_claude_response_includes_history():
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text='Reply')]
    mock_message.usage.input_tokens = 10
    mock_message.usage.output_tokens = 5
    mock_client.messages.create.return_value = mock_message

    history = [
        {'role': 'user', 'content': 'First message'},
        {'role': 'assistant', 'content': 'First reply'},
    ]
    with patch('claude_handler.client', mock_client):
        get_claude_response(SAMPLE_CONTEXT, history, 'Second message')
        call_args = mock_client.messages.create.call_args
        messages = call_args.kwargs['messages']
        # Should include history + new user message = 3 total
        assert len(messages) == 3
        assert messages[-1]['role'] == 'user'
        assert messages[-1]['content'] == 'Second message'


def test_get_claude_response_empty_history():
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text='First response')]
    mock_message.usage.input_tokens = 20
    mock_message.usage.output_tokens = 10
    mock_client.messages.create.return_value = mock_message

    with patch('claude_handler.client', mock_client):
        response, tokens = get_claude_response(SAMPLE_CONTEXT, [], 'First message')
        call_args = mock_client.messages.create.call_args
        messages = call_args.kwargs['messages']
        assert len(messages) == 1
        assert messages[0]['role'] == 'user'
        assert tokens == 30


def _mock_message(text='ok', in_tokens=1, out_tokens=1):
    m = MagicMock()
    m.content = [MagicMock(text=text)]
    m.usage.input_tokens = in_tokens
    m.usage.output_tokens = out_tokens
    return m


def test_get_claude_response_uses_default_model_when_not_specified():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_message()
    with patch('claude_handler.client', mock_client):
        get_claude_response(SAMPLE_CONTEXT, [], 'Hello')
        assert mock_client.messages.create.call_args.kwargs['model'] == claude_handler.MODEL


def test_get_claude_response_passes_explicit_model():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_message()
    with patch('claude_handler.client', mock_client):
        get_claude_response(SAMPLE_CONTEXT, [], 'Hello', model='claude-haiku-4-5-20251001')
        assert mock_client.messages.create.call_args.kwargs['model'] == 'claude-haiku-4-5-20251001'


def test_get_claude_response_passes_persona_into_system_prompt():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_message()
    with patch('claude_handler.client', mock_client):
        get_claude_response(SAMPLE_CONTEXT, [], 'Hello', persona=SAMPLE_PERSONA)
    system = mock_client.messages.create.call_args.kwargs['system']
    assert SAMPLE_PERSONA in system[0]['text']


def test_stream_claude_response_passes_persona_into_system_prompt():
    mock_client = MagicMock()
    fake_stream = MagicMock()
    fake_stream.text_stream = iter(['a'])
    fake_stream.get_final_message.return_value = _mock_message()
    mock_client.messages.stream.return_value.__enter__.return_value = fake_stream
    mock_client.messages.stream.return_value.__exit__.return_value = False

    with patch('claude_handler.client', mock_client):
        list(stream_claude_response(SAMPLE_CONTEXT, [], 'Hello', persona=SAMPLE_PERSONA))
    system = mock_client.messages.stream.call_args.kwargs['system']
    assert SAMPLE_PERSONA in system[0]['text']


def test_system_block_is_cached_with_one_hour_ttl():
    """The system prompt is byte-stable per (skin, module), so it ships as a
    single cached block — every student in the cohort shares one entry."""
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_message()
    with patch('claude_handler.client', mock_client):
        get_claude_response(SAMPLE_CONTEXT, [], 'Hello')
    system = mock_client.messages.create.call_args.kwargs['system']
    assert len(system) == 1, 'one block keeps the whole prompt in the cached prefix'
    assert system[0]['cache_control'] == {'type': 'ephemeral', 'ttl': '1h'}


def test_identical_inputs_produce_byte_identical_system_block():
    """Cache hits are a prefix match — any per-request drift (a timestamp,
    unsorted iteration) would silently cost the cohort full price."""
    a = build_system_prompt(SAMPLE_CONTEXT, SAMPLE_PERSONA)
    b = build_system_prompt(SAMPLE_CONTEXT, SAMPLE_PERSONA)
    assert a == b


def test_token_total_includes_cache_tokens():
    """Once the prompt is cached, the corpus leaves input_tokens for the
    cache counters. Summing only input+output would under-bill a cohort by
    the size of the whole module window on every cached message."""
    mock_client = MagicMock()
    message = _mock_message(in_tokens=10, out_tokens=5)
    message.usage.cache_creation_input_tokens = 0
    message.usage.cache_read_input_tokens = 8000
    mock_client.messages.create.return_value = message

    with patch('claude_handler.client', mock_client):
        _, tokens = get_claude_response(SAMPLE_CONTEXT, [], 'Hello')
    assert tokens == 8015


def test_token_total_tolerates_null_cache_fields():
    """The SDK types the cache counters Optional — a None must not blow up
    the budget write on a request that never touched the cache."""
    mock_client = MagicMock()
    message = _mock_message(in_tokens=10, out_tokens=5)
    message.usage.cache_creation_input_tokens = None
    message.usage.cache_read_input_tokens = None
    mock_client.messages.create.return_value = message

    with patch('claude_handler.client', mock_client):
        _, tokens = get_claude_response(SAMPLE_CONTEXT, [], 'Hello')
    assert tokens == 15


def test_stream_claude_response_passes_explicit_model():
    mock_client = MagicMock()
    fake_stream = MagicMock()
    fake_stream.text_stream = iter(['chunk1', 'chunk2'])
    final = MagicMock()
    final.usage.input_tokens = 3
    final.usage.output_tokens = 4
    fake_stream.get_final_message.return_value = final
    mock_client.messages.stream.return_value.__enter__.return_value = fake_stream
    mock_client.messages.stream.return_value.__exit__.return_value = False

    with patch('claude_handler.client', mock_client):
        chunks = list(stream_claude_response(
            SAMPLE_CONTEXT, [], 'Hello', model='claude-haiku-4-5-20251001'
        ))
    assert mock_client.messages.stream.call_args.kwargs['model'] == 'claude-haiku-4-5-20251001'
    # final tuple is ('', total_tokens)
    assert chunks[-1] == ('', 7)
