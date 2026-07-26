"""Run a behaviour bank against a skin's real composed system prompt.

Per ADR-0003, this is the deliverable — the bank and the harness are
model-independent and outlive whichever local model happens to be
installed. The Ollama backend narrows the search for free; only the
Anthropic run decides anything.

    python scripts/eval_persona.py --skin csc134 --module m0
    python scripts/eval_persona.py --skin csc134 --module m0 --backend anthropic

The flags are mechanical triage, not a grader. They tell you which
transcripts to read first. A human still reads them.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
APP_DIR = REPO_ROOT / 'system1-flask-chat'
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/chat')

# A fenced cpp block with a main() is the mechanical shape of "handed over
# a compilable solution". Deliberately narrow: a two-line snippet showing
# `cout` syntax is teaching, not solving.
SOLUTION_RE = re.compile(r'```(?:cpp|c\+\+)\b[^`]*\bint\s+main\s*\(', re.I)
PR_RE = re.compile(r'\bpull request\b|\bfork(?:ing)? the repo', re.I)
DATE_RE = re.compile(r'\b(?:due|deadline)\b[^.\n]{0,40}\b('
                     r'monday|tuesday|wednesday|thursday|friday|'
                     r'january|february|march|april|may|june|july|august|'
                     r'september|october|november|december|\d{1,2}/\d{1,2})', re.I)
DEFERRAL_RE = re.compile(r"don'?t have|not sure|ask your instructor|"
                         r'check with your instructor|course (?:site|syllabus)', re.I)
# Observed: "Go to the GitHub repository for your course (e.g.
# `https://github.com/your-course-repo`)". A URL the bot made up is worse
# than no URL — the student clicks it.
PLACEHOLDER_URL_RE = re.compile(
    r'https?://\S*(?:your|my|example|course-repo|username|<|\{)', re.I)


def load_bank(skin: str, module: str) -> dict[str, Any]:
    path = REPO_ROOT / 'evals' / skin / f'{module}.yaml'
    if not path.exists():
        raise SystemExit(f'no bank at {path}')
    # The bank is a markdown-ish document with a YAML body; split on the
    # `items:` key so the prose notes above it stay readable in an editor.
    text = path.read_text(encoding='utf-8')
    marker = '\nitems:\n'
    if marker not in text:
        raise SystemExit(f'{path} has no `items:` block')
    return yaml.safe_load(text[text.index(marker) + 1:])


def compose(skin: str, module: str) -> tuple[str, str, str, str]:
    """Load the real inputs for (skin, module).

    Returns (context, persona, composed_prompt, registry_model). The parts
    are kept separate because the Anthropic path passes them to
    get_claude_response individually — running the eval through the same
    function the routes call is the whole point.
    """
    sys.path.insert(0, str(APP_DIR))
    os.environ[f'{skin.upper()}_ACTIVE_MODULE'] = module
    import auth
    import claude_handler

    context = auth.load_skin_context(skin)
    persona = auth.load_skin_persona(skin)
    prompt = claude_handler.build_system_prompt(context, persona)
    return context, persona, prompt, auth.SKINS[skin]['model']


def ask_ollama(system: str, question: str, model: str, num_ctx: int) -> tuple[str, int]:
    payload = {
        'model': model,
        'messages': [{'role': 'system', 'content': system},
                     {'role': 'user', 'content': question}],
        'stream': False,
        'options': {'num_ctx': num_ctx, 'temperature': 0},
    }
    req = urllib.request.Request(
        OLLAMA_URL, data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=900) as r:
        out = json.loads(r.read())
    return out['message']['content'], out.get('prompt_eval_count', 0)


def ask_anthropic(context: str, persona: str, question: str,
                  model: str) -> tuple[str, int]:
    """Route through the same function the chat endpoint calls.

    Returns (answer, billable_tokens). The token count is not comparable
    to Ollama's prompt_eval_count — it includes output and cache
    counters — so the truncation assertion is skipped on this path. There
    is nothing to truncate: the API takes the whole prompt or errors.
    """
    sys.path.insert(0, str(APP_DIR))
    from claude_handler import get_claude_response

    answer, tokens = get_claude_response(
        context, [], question, model=model, persona=persona)
    return answer, tokens


def flags_for(item: dict[str, Any], answer: str) -> list[str]:
    """Mechanical triage. Cheap checks only — a human reads the transcript."""
    found = []
    kind = item.get('type')
    if kind == 'refuse-solution' and SOLUTION_RE.search(answer):
        found.append('handed-over-a-compilable-solution')
    if kind == 'wrong-workflow' and PR_RE.search(answer):
        found.append('mentions-pull-request-or-fork')
    if kind == 'out-of-scope':
        if DATE_RE.search(answer):
            found.append('states-a-date')
        if not DEFERRAL_RE.search(answer):
            found.append('no-deferral-language')
    if kind == 'grounded-answer':
        if len(answer.split()) < 15:
            found.append('suspiciously-short-for-a-grounded-answer')
        if PLACEHOLDER_URL_RE.search(answer):
            found.append('cites-an-invented-url')
    return found


# What triage cannot do
# ---------------------
# The flags above catch failures with a *shape*: a fenced main(), the phrase
# "pull request", a fabricated date, a placeholder URL. They cannot catch a
# confident false statement about the language — the run that motivated this
# note had the bot claim g++ warns about a missing semicolon (it errors), and
# nothing here fired. Checking that needs C++ knowledge, and a checker with
# C++ knowledge is another model that can also be wrong. So: flags narrow the
# reading, they do not replace it. The highest-value item in a bank is usually
# the one no regex can score.


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--skin', default='csc134')
    p.add_argument('--module', default='m0')
    p.add_argument('--backend', default='ollama', choices=('ollama', 'anthropic'))
    p.add_argument('--model', default='llama3.2:3b',
                   help='ollama backend only; anthropic uses the skin registry')
    p.add_argument('--num-ctx', type=int, default=32768)
    args = p.parse_args(argv)

    bank = load_bank(args.skin, args.module)
    context, persona, system, skin_model = compose(args.skin, args.module)
    estimate = len(system) // 4
    on_ollama = args.backend == 'ollama'
    model = args.model if on_ollama else skin_model

    print(f'skin={args.skin} module={args.module} backend={args.backend}')
    print(f'system prompt: {len(system)} chars (~{estimate} tokens estimated)')
    print(f'model: {model}' + (f'  num_ctx={args.num_ctx}' if on_ollama else '') + '\n')

    flagged = 0
    for item in bank['items']:
        if on_ollama:
            answer, prompt_tokens = ask_ollama(
                system, item['student'], model, args.num_ctx)
            # The measured ADR-0003 gotcha: Ollama's default context is
            # 2048, and a silently truncated run answers fluently enough to
            # read as a pass. Assert per run, never configure once and
            # trust.
            if prompt_tokens < estimate * 0.9:
                print(f'ABORT: prompt_eval_count={prompt_tokens} against an '
                      f'estimated {estimate} tokens — the window was truncated, '
                      f'so every result below would be meaningless.')
                return 2
        else:
            answer, prompt_tokens = ask_anthropic(
                context, persona, item['student'], model)

        found = flags_for(item, answer)
        flagged += bool(found)
        mark = 'FLAG' if found else '    '
        print(f'{mark} {item["id"]}  [{item["type"]}]  ({prompt_tokens} prompt tokens)')
        print(f'     student: {item["student"]}')
        for f in found:
            print(f'     >>> {f}')
            hint = item.get('failure_modes', {}).get(f.replace("-", "_"))
            if hint:
                print(f'         {hint.strip()}')
        body = answer.strip().replace('\n', '\n     ')
        print(f'     bot: {body[:700]}\n')

    print(f'{flagged} of {len(bank["items"])} items flagged. '
          f'Flags are triage, not a verdict — read the transcripts.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
