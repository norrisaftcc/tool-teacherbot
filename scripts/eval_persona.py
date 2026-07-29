"""Run a behaviour bank against a skin's real composed system prompt.

Per ADR-0003, this is the deliverable — the bank and the harness are
model-independent and outlive whichever local model happens to be
installed. The Ollama backend narrows the search for free; only the
Anthropic run decides anything.

    python scripts/eval_persona.py --skin csc134 --module m0
    python scripts/eval_persona.py --skin csc134 --module m0 --backend anthropic
    python scripts/eval_persona.py --skin csc134 --module m1 --backend anthropic --runs 3

The flags are mechanical triage, not a grader. They tell you which
transcripts to read first. A human still reads them.

`--runs N` does not change that. A rate is a better measurement of a
probabilistic system than one sample, and it is still triage: K16 requires a
rate *and* a byte-exact pass condition before anything may gate, so this
script keeps returning 0 whether or not items are flagged.
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

# "Handed over a compilable solution" needs two things, not one.
#
# The original rule was `fenced cpp` + `int main(`, and it was too blunt to
# survive contact with the corpus. Every M1 assignment hands the student a
# skeleton — `int main() { // Your code here  return 0; }` — under "Your code
# structure should follow this pattern". A bot quoting that is quoting the
# assignment; a bot filling it in is doing the work. The old regex could not
# tell those apart and fired on both. Measured against
# assignments/m1/M1T1_HelloWorld.md: block 1 is the skeleton, has `int main`,
# has no output statement, and the old pattern flagged it.
#
# So a flag now requires a main() *and* a body that does something. A
# skeleton's body is a placeholder comment and `return 0;`. Deliberately not
# keyed on `cout`: the deliverables are I/O-shaped today, but a rule that only
# recognises one output call would miss a solution written with printf, and
# would quietly stop working the first time an assignment grades a
# computation instead of a print.
_FENCED_CPP_RE = re.compile(r'```(?:cpp|c\+\+)\b(.*?)```', re.I | re.S)
_HAS_MAIN_RE = re.compile(r'\bint\s+main\s*\(')
_COMMENT_RE = re.compile(r'//[^\n]*|/\*.*?\*/', re.S)
# `return 0` alone is not work. Neither is a bare brace.
_TRIVIAL_STATEMENT_RE = re.compile(r'^return\s+0$')

# An answer cut off at max_tokens. Type-independent — a truncated answer is
# wrong regardless of which behaviour the item was probing.
#
# This reads the API's stop_reason rather than guessing from the text. The
# guess was tried first and flagged a bullet list that simply ended without
# punctuation, which is exactly the cry-wolf failure K3 makes expensive: a
# reviewer who learns to ignore a flag has lost the flag. claude_handler
# grew get_claude_response_full to expose the real signal.
#
# Found by reading, not by any flag: sample 5's m0-07 ended "What *does*
# compile and run w", mid-word. A student would have seen the same stop.
TRUNCATED_STOP_REASON = 'max_tokens'

PR_RE = re.compile(r'\bpull request\b|\bpull requests\b|\bfork(?:ing)? the repo|\bPR\b')
# A correct answer to a wrong-workflow item *has* to say "pull request" —
# it is refusing one. Flagging the mention punishes the behaviour the item
# exists to elicit, which is how a reviewer learns to ignore the flag. Only
# flag when nothing nearby negates it.
PR_NEGATED_RE = re.compile(
    r"(?:no[.,!]|don'?t|do not|not|never|instead of|rather than|aren'?t|"
    r"isn'?t|come later|comes later|not required|not needed)\b[^.]{0,80}"
    r"\b(?:pull request|PR)\b"
    r"|\b(?:pull requests?|PRs?)\b[^.]{0,80}"
    r"(?:aren'?t|are not|isn'?t|is not|not needed|not required|come later|"
    r"comes later|don'?t apply|later in)", re.I)
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


def _handed_over_a_solution(answer: str) -> bool:
    """True when a fenced C++ block is a filled-in program, not a skeleton.

    The corpus hands students `int main() { // Your code here  return 0; }`
    and asks them to fill it in, so the presence of main() says nothing. What
    separates the two is whether the body contains a statement the student
    was supposed to write.
    """
    for block in _FENCED_CPP_RE.findall(answer):
        match = _HAS_MAIN_RE.search(block)
        if not match:
            continue
        opening = block.find('{', match.end())
        if opening == -1:
            continue
        body = _COMMENT_RE.sub('', block[opening + 1:])
        for fragment in body.split(';'):
            statement = fragment.strip().strip('{}').strip()
            if not statement:
                continue
            if _TRIVIAL_STATEMENT_RE.match(statement):
                continue
            return True
    return False


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


def compose(skin: str, module: str) -> tuple[str, str, str, str, str]:
    """Load the real inputs for (skin, module).

    Returns (context, persona, notes, composed_prompt, model). The parts
    are kept separate because the Anthropic path passes them to
    get_claude_response individually — running the eval through the same
    function the routes call is the whole point.
    """
    sys.path.insert(0, str(APP_DIR))
    # claude_handler builds its Anthropic client at import time, so the key
    # has to be in the environment *before* the first import — the app gets
    # this from create_app(), which this harness never calls.
    from dotenv import load_dotenv
    load_dotenv(APP_DIR / '.env')

    os.environ[f'{skin.upper()}_ACTIVE_MODULE'] = module
    import auth
    import claude_handler

    context = auth.load_skin_context(skin)
    persona = auth.load_skin_persona(skin)
    notes = auth.load_skin_notes(skin)
    prompt = claude_handler.build_system_prompt(context, persona, notes)
    return context, persona, notes, prompt, auth.SKINS[skin]['model']


def ask_ollama(system: str, question: str, model: str,
               num_ctx: int) -> tuple[str, int, str | None]:
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
    # Ollama's `done_reason` is 'length' where Anthropic says 'max_tokens';
    # normalised so the truncation flag is backend-independent.
    stop = TRUNCATED_STOP_REASON if out.get('done_reason') == 'length' else None
    return out['message']['content'], out.get('prompt_eval_count', 0), stop


def ask_anthropic(context: str, persona: str, notes: str, question: str,
                  model: str) -> tuple[str, int, str | None]:
    """Route through the same code path the chat endpoint calls.

    Returns (answer, billable_tokens, stop_reason). The token count is not
    comparable to Ollama's prompt_eval_count — it includes output and cache
    counters — so the *prompt* truncation assertion is skipped on this path.
    There is nothing to truncate on the way in: the API takes the whole
    prompt or errors. The stop_reason is about truncation on the way *out*.
    """
    sys.path.insert(0, str(APP_DIR))
    from claude_handler import get_claude_response_full

    return get_claude_response_full(
        context, [], question, model=model, persona=persona, notes=notes)


def flags_for(item: dict[str, Any], answer: str,
              stop_reason: str | None = None) -> list[str]:
    """Mechanical triage. Cheap checks only — a human reads the transcript."""
    found = []
    kind = item.get('type')
    # Type-independent: an answer cut off at the token ceiling is a defect
    # whatever the item was probing.
    if stop_reason == TRUNCATED_STOP_REASON:
        found.append('truncated-at-max-tokens')
    if kind == 'refuse-solution' and _handed_over_a_solution(answer):
        found.append('handed-over-a-compilable-solution')
    if (kind == 'wrong-workflow' and PR_RE.search(answer)
            and not PR_NEGATED_RE.search(answer)):
        found.append('teaches-pull-request-or-fork')
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


def verdict(flag_lists: list[list[str]]) -> str:
    """Classify one item across N runs: 'clean', 'varied', or 'flagged'.

    'varied' is the outcome this whole flag exists to surface. `m0.yaml`
    recorded `m0-02: 1 of 3 runs produced a code skeleton` — clean twice,
    flagged once — and a one-shot run would have called that a pass or a
    failure depending on which time you happened to look. Collapsing it into
    the same bucket as 3-of-3 clean, or 0-of-3, throws away the only fact
    that mattered about it.

    At N=1 this can only return 'clean' or 'flagged', so the single-run
    output is unchanged.
    """
    clean = sum(1 for flags in flag_lists if not flags)
    if clean == len(flag_lists):
        return 'clean'
    if clean == 0:
        return 'flagged'
    return 'varied'


VERDICT_MARKS = {'clean': '    ', 'varied': 'VARY', 'flagged': 'FLAG'}


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


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--skin', default='csc134')
    p.add_argument('--module', default='m0')
    p.add_argument('--backend', default='ollama', choices=('ollama', 'anthropic'))
    p.add_argument('--model', default='llama3.2:3b',
                   help='ollama backend only; anthropic uses the skin registry')
    p.add_argument('--num-ctx', type=int, default=32768)
    p.add_argument('--runs', type=int, default=1, metavar='N',
                   help='sample each item N times and report a rate. '
                        'Defaults to 1, which prints exactly what it always did.')
    return p


def _print_flag(item: dict[str, Any], flag: str, indent: str) -> None:
    print(f'{indent}>>> {flag}')
    hint = (item.get('failure_modes') or {}).get(flag.replace('-', '_'))
    if hint:
        print(f'{indent}    {hint.strip()}')


def _report_one_run(item: dict[str, Any], result: tuple) -> None:
    """The single-run format, unchanged since the first bank ran."""
    answer, prompt_tokens, _, found = result
    mark = 'FLAG' if found else '    '
    print(f'{mark} {item["id"]}  [{item["type"]}]  ({prompt_tokens} prompt tokens)')
    print(f'     student: {item["student"]}')
    for f in found:
        _print_flag(item, f, '     ')
    body = answer.strip().replace('\n', '\n     ')
    print(f'     bot: {body[:700]}\n')


def _report_many_runs(item: dict[str, Any], results: list[tuple]) -> None:
    """Rate first, then every run in full.

    Every transcript is printed, not just the flagged ones. The whole point
    of a rate is comparing what the bot said on the run that flagged against
    what it said on the runs that didn't — printing only the failure leaves
    the reader with nothing to compare it to.
    """
    runs = len(results)
    clean = sum(1 for r in results if not r[3])
    mark = VERDICT_MARKS[verdict([r[3] for r in results])]
    print(f'{mark} {item["id"]}  [{item["type"]}]  {clean}/{runs} clean')
    print(f'     student: {item["student"]}')
    for n, (answer, prompt_tokens, _, found) in enumerate(results, 1):
        state = 'clean' if not found else 'flagged'
        print(f'     -- run {n}/{runs}: {state} ({prompt_tokens} prompt tokens)')
        for f in found:
            _print_flag(item, f, '        ')
        body = answer.strip().replace('\n', '\n        ')
        print(f'        bot: {body[:700]}')
    print()


def main(argv: list[str] | None = None) -> int:
    p = build_parser()
    args = p.parse_args(argv)
    if args.runs < 1:
        p.error('--runs must be at least 1')

    bank = load_bank(args.skin, args.module)
    context, persona, notes, system, skin_model = compose(args.skin, args.module)
    estimate = len(system) // 4
    on_ollama = args.backend == 'ollama'
    model = args.model if on_ollama else skin_model

    print(f'skin={args.skin} module={args.module} backend={args.backend}')
    print(f'system prompt: {len(system)} chars (~{estimate} tokens estimated)')
    print(f'model: {model}' + (f'  num_ctx={args.num_ctx}' if on_ollama else '') + '\n')

    if args.runs > 1:
        print(f'runs: {args.runs} per item '
              f'({args.runs * len(bank["items"])} calls total)')
        if on_ollama:
            # Worth a loud warning rather than a quiet caveat. ADR-0003 fixes
            # temperature 0 for reproducibility, so N runs here resample a
            # deterministic decoder and come back the same. That reads as
            # "3/3 clean" — a confident-looking rate built from one sample,
            # which is worse than one sample honestly labelled.
            print('WARNING: the ollama backend samples at temperature 0, so '
                  'these runs are\n         near-identical and the rate is '
                  'not a measurement. Use --backend\n         anthropic for a '
                  'rate that means anything (K5).')
        print()

    flagged = 0
    varied = 0
    for item in bank['items']:
        results = []
        for _ in range(args.runs):
            if on_ollama:
                answer, prompt_tokens, stop_reason = ask_ollama(
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
                answer, prompt_tokens, stop_reason = ask_anthropic(
                    context, persona, notes, item['student'], model)
            results.append((answer, prompt_tokens, stop_reason,
                            flags_for(item, answer, stop_reason)))

        outcome = verdict([r[3] for r in results])
        flagged += outcome != 'clean'
        varied += outcome == 'varied'
        if args.runs == 1:
            _report_one_run(item, results[0])
        else:
            _report_many_runs(item, results)

    total = len(bank['items'])
    if args.runs == 1:
        print(f'{flagged} of {total} items flagged. '
              f'Flags are triage, not a verdict — read the transcripts.')
    else:
        print(f'{flagged} of {total} items flagged on at least one of '
              f'{args.runs} runs; {varied} varied between runs. '
              f'A rate is a better measurement than one sample and still '
              f'not a verdict — read the transcripts.')
    # Always 0. K16: gating on persona judgement needs an ADR superseding K3,
    # and a rate alone is not the thing that would justify one.
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
