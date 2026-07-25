# tests/test_claude_handler.py
from unittest.mock import MagicMock, patch
import claude_handler
from claude_handler import (
    build_system_prompt,
    get_claude_response,
    stream_claude_response,
)

SAMPLE_CONTEXT = """
# Group 1 Context
## Project Overview
- Product: DataMan Math Platform
- Tech Stack: Flask, SQLite, React
"""


def test_system_prompt_contains_context():
    prompt = build_system_prompt(SAMPLE_CONTEXT)
    assert 'DataMan' in prompt


def test_system_prompt_contains_pedagogical_guardrails():
    prompt = build_system_prompt(SAMPLE_CONTEXT)
    # Must contain either Sacred Workflow reference or anti-direct-solution guidance
    assert 'Sacred Workflow' in prompt or 'direct solution' in prompt.lower()


def test_system_prompt_contains_vocabulary_rules():
    prompt = build_system_prompt(SAMPLE_CONTEXT)
    assert 'growth opportunity' in prompt.lower() or 'suboptimal' in prompt.lower()


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
