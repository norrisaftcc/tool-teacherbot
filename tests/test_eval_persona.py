"""Tests for the behaviour-bank harness (ADR-0003).

These check the harness and the bank's shape. They do not call a model —
whether the bot passes the bank is a question for a run, not a unit test.
"""
from pathlib import Path

import pytest

import scripts.eval_persona as ev

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED = {'id', 'type', 'probes', 'student', 'expect', 'must_not'}


def test_csc134_m0_bank_parses_and_is_complete():
    bank = ev.load_bank('csc134', 'm0')
    assert bank['items'], 'bank has no items'
    for item in bank['items']:
        missing = REQUIRED - set(item)
        assert not missing, f'{item.get("id")} missing {missing}'
        assert item['student'] == item['student'].strip()
        # Every predicted failure needs a diagnosis, per the M4 answer-key
        # pattern: a failure mode without a "why" is a score, not feedback.
        for name, why in (item.get('failure_modes') or {}).items():
            assert why.strip(), f'{item["id"]}/{name} has no explanation'


def test_bank_item_ids_are_unique():
    ids = [i['id'] for i in ev.load_bank('csc134', 'm0')['items']]
    assert len(ids) == len(set(ids)), f'duplicate ids in bank: {ids}'


def test_missing_bank_exits_cleanly():
    with pytest.raises(SystemExit):
        ev.load_bank('csc134', 'no-such-module')


# ---- the mechanical flags ---------------------------------------------------

def test_flags_a_handed_over_solution():
    item = {'type': 'refuse-solution'}
    answer = 'Sure:\n```cpp\n#include <iostream>\nint main() { return 0; }\n```'
    assert 'handed-over-a-compilable-solution' in ev.flags_for(item, answer)


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
