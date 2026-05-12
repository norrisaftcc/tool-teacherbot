import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

MODEL = 'claude-sonnet-4-6'
MAX_TOKENS = 1024


def build_system_prompt(group_context: str) -> str:
    return f"""You are an AI teaching assistant for the AlgoCratic Futures capstone course.

CURRENT GROUP CONTEXT:
{group_context}

PEDAGOGICAL RULES:
1. Never provide direct solutions — guide students through iteration
2. Ask students to explain their attempt before you help
3. Ask clarifying questions before answering
4. Emphasize the Sacred Workflow: Issue → Branch → PR → Review → Merge
5. Reference the group's specific project context when relevant
6. Celebrate iteration and learning velocity, not just correct answers

VOCABULARY:
- Say "growth opportunity" not "error"
- Say "suboptimal" not "wrong"
- Say "The Algorithm suggests" not "You should"

RESPONSE STYLE:
- Technical but encouraging
- Light AlgoCratic voice (5% seasoning — don't overdo it)
- Competence and clarity over entertainment
"""


def get_claude_response(
    group_context: str,
    history: list[dict],
    user_message: str,
) -> tuple[str, int]:
    """
    Call Claude with context and conversation history.

    Args:
        group_context: The group's project context markdown string
        history: List of {'role': 'user'|'assistant', 'content': str} dicts
        user_message: The new message from the student

    Returns:
        (response_text, total_tokens_used)
    """
    messages = history + [{'role': 'user', 'content': user_message}]

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=build_system_prompt(group_context),
        messages=messages,
    )

    text = response.content[0].text
    tokens = response.usage.input_tokens + response.usage.output_tokens
    return text, tokens
