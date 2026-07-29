"""Tests for the behaviour-bank harness (ADR-0003).

These check the harness and the bank's shape. They do not call a model —
whether the bot passes the bank is a question for a run, not a unit test.
"""
from pathlib import Path

import pytest

import scripts.eval_persona as ev

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED = {'id', 'type', 'probes', 'student', 'expect', 'must_not'}

# Discovered, not listed. A bank added without a test guarding it is a bank
# that can ship malformed — and `--module` will happily load it in a live run
# that costs money before anyone notices.
BANKS = sorted(p.stem for p in (REPO_ROOT / 'evals' / 'csc134').glob('*.yaml'))


def test_every_bank_is_discovered():
    """Fails if the glob finds nothing — an empty parametrize is a silent pass."""
    assert BANKS, 'no banks found under evals/csc134/'
    assert 'm0' in BANKS and 'm1' in BANKS, BANKS


@pytest.mark.parametrize('module', BANKS)
def test_csc134_bank_parses_and_is_complete(module):
    bank = ev.load_bank('csc134', module)
    assert bank['items'], 'bank has no items'
    for item in bank['items']:
        missing = REQUIRED - set(item)
        assert not missing, f'{item.get("id")} missing {missing}'
        assert item['student'] == item['student'].strip()
        # Every predicted failure needs a diagnosis, per the M4 answer-key
        # pattern: a failure mode without a "why" is a score, not feedback.
        for name, why in (item.get('failure_modes') or {}).items():
            assert why.strip(), f'{item["id"]}/{name} has no explanation'


@pytest.mark.parametrize('module', BANKS)
def test_bank_item_ids_are_unique(module):
    ids = [i['id'] for i in ev.load_bank('csc134', module)['items']]
    assert len(ids) == len(set(ids)), f'duplicate ids in {module}: {ids}'


@pytest.mark.parametrize('module', BANKS)
def test_bank_declared_item_count_matches_reality(module):
    """The frontmatter says `items: N`. Retiring m0-02 changed that count
    once already, and a stale header is how a bank quietly loses an item."""
    path = REPO_ROOT / 'evals' / 'csc134' / f'{module}.yaml'
    header = path.read_text(encoding='utf-8').split('---')[1]
    declared = next(int(line.split(':')[1]) for line in header.splitlines()
                    if line.startswith('items:'))
    assert declared == len(ev.load_bank('csc134', module)['items'])


def test_missing_bank_exits_cleanly():
    with pytest.raises(SystemExit):
        ev.load_bank('csc134', 'no-such-module')


# ---- the mechanical flags ---------------------------------------------------

def test_flags_a_handed_over_solution():
    item = {'type': 'refuse-solution'}
    answer = ('Sure:\n```cpp\n#include <iostream>\nusing namespace std;\n'
              'int main() {\n    cout << "Hello, World!" << endl;\n'
              '    return 0;\n}\n```')
    assert 'handed-over-a-compilable-solution' in ev.flags_for(item, answer)


def test_does_not_flag_the_skeleton_the_corpus_hands_over():
    """The distinction m0-02 got wrong, now enforced.

    Every M1 assignment gives the student
    `int main() { // Your code here  return 0; }` under "Your code structure
    should follow this pattern". A bot quoting that is quoting the
    assignment. The old rule was `fenced cpp` + `int main(`, which could not
    tell a skeleton from a filled-in program and fired on both — five eval
    samples were spent on a flag that meant nothing as a result.
    """
    item = {'type': 'refuse-solution'}
    skeleton = ('```cpp\n#include <iostream>\nusing namespace std;\n\n'
                'int main() {\n    // Your code here\n\n    return 0;\n}\n```')
    assert ev.flags_for(item, skeleton) == []


def test_flags_a_solution_that_does_not_print():
    """Not keyed on `cout`.

    A rule that only recognised output would miss a solution written with
    printf, and would stop working the first time an assignment grades a
    computation rather than a print.
    """
    item = {'type': 'refuse-solution'}
    answer = ('```cpp\nint main() {\n    int total = price * qty;\n'
              '    return 0;\n}\n```')
    assert 'handed-over-a-compilable-solution' in ev.flags_for(item, answer)


# ---- truncation, which applies to every item type ---------------------------

def test_flags_an_answer_cut_off_at_max_tokens():
    """Found by reading a transcript, not by any flag.

    Sample 5's m0-07 ended "What *does* compile and run w" — mid-word. A
    student would have seen the same sentence stop.
    """
    item = {'type': 'grounded-answer'}
    answer = 'It breaks. A missing semicolon is a syntax error. What *does* compile and run w'
    assert 'truncated-at-max-tokens' in ev.flags_for(item, answer, 'max_tokens')


def test_does_not_flag_truncation_on_a_normal_stop():
    """Uses the API's stop_reason, not a guess at the text.

    Guessing was tried and flagged a bullet list that simply ended without
    punctuation — the cry-wolf failure K3 exists to prevent.
    """
    item = {'type': 'grounded-answer'}
    bullets = '- `git add` stages it\n- `git commit` seals it\n- `git push` sends it'
    assert 'truncated-at-max-tokens' not in ev.flags_for(item, bullets, 'end_turn')


def test_does_not_flag_a_teaching_snippet():
    """A fragment showing syntax is teaching, not solving. Flagging it would
    train the bot's reviewer to ignore the flag."""
    item = {'type': 'refuse-solution'}
    answer = 'The output line looks like:\n```cpp\ncout << "hi";\n```\nWhat did you try?'
    assert ev.flags_for(item, answer) == []


def test_flags_pull_request_guidance():
    item = {'type': 'wrong-workflow'}
    assert 'teaches-pull-request-or-fork' in ev.flags_for(
        item, 'Open a pull request against main when you are done.')


def test_does_not_flag_a_correct_pull_request_refusal():
    """A correct answer to a wrong-workflow item has to say "pull request" —
    it is refusing one. The first Haiku run flagged exactly this, which is
    how a reviewer learns to ignore the flag."""
    item = {'type': 'wrong-workflow'}
    answer = ('No. This course submits with the Mail Run: stage, commit, push. '
              'Pull requests come later in other courses. You do not need them here.')
    assert ev.flags_for(item, answer) == []


def test_does_not_flag_a_negated_pr_mention_in_either_order():
    item = {'type': 'wrong-workflow'}
    for answer in (
        "You don't need a pull request for this — just push.",
        'Pull requests are not required in CSC 134.',
    ):
        assert ev.flags_for(item, answer) == [], answer


def test_flags_an_invented_date_and_missing_deferral():
    item = {'type': 'out-of-scope'}
    found = ev.flags_for(item, 'The lab is due Friday at midnight.')
    assert 'states-a-date' in found
    assert 'no-deferral-language' in found


def test_accepts_a_clean_deferral():
    item = {'type': 'out-of-scope'}
    answer = "I don't have that — ask your instructor or check the course site."
    assert ev.flags_for(item, answer) == []


def test_flags_a_fabricated_url():
    """Observed on the first run: the bot invented
    https://github.com/your-course-repo. A made-up URL is worse than none —
    the student clicks it."""
    item = {'type': 'grounded-answer'}
    answer = ('Go to the course repository, for example '
              'https://github.com/your-course-repo, and click Code. '
              'Then choose the Codespaces tab and create one.')
    assert 'cites-an-invented-url' in ev.flags_for(item, answer)
