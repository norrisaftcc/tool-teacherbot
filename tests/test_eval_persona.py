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
#
# Both skins are discovered from `evals/*/*.yaml`. The csc134 path used to be
# hard-coded, so a cts285 bank would have shipped with no shape test at all.
BANK_PAIRS = sorted(
    (p.parent.name, p.stem) for p in (REPO_ROOT / 'evals').glob('*/*.yaml'))
BANKS = sorted(m for s, m in BANK_PAIRS if s == 'csc134')
CTS285_BANKS = sorted(m for s, m in BANK_PAIRS if s == 'cts285')
BANK_IDS = [f'{s}/{m}' for s, m in BANK_PAIRS]


def test_every_bank_is_discovered():
    """Fails if the glob finds nothing — an empty parametrize is a silent pass."""
    assert BANK_PAIRS, 'no banks found under evals/'
    assert 'm0' in BANKS and 'm1' in BANKS, BANKS


def test_cts285_banks_are_discovered():
    """The non-empty assert for the second skin. Without it a deleted or
    renamed cts285 directory leaves every parametrized test below with fewer
    cases and nothing red."""
    assert CTS285_BANKS == ['m1', 'm2', 'm3'], CTS285_BANKS


@pytest.mark.parametrize('skin,module', BANK_PAIRS, ids=BANK_IDS)
def test_bank_parses_and_is_complete(skin, module):
    bank = ev.load_bank(skin, module)
    assert bank['items'], 'bank has no items'
    for item in bank['items']:
        missing = REQUIRED - set(item)
        assert not missing, f'{item.get("id")} missing {missing}'
        assert item['student'] == item['student'].strip()
        # Every predicted failure needs a diagnosis, per the M4 answer-key
        # pattern: a failure mode without a "why" is a score, not feedback.
        for name, why in (item.get('failure_modes') or {}).items():
            assert why.strip(), f'{item["id"]}/{name} has no explanation'


@pytest.mark.parametrize('skin,module', BANK_PAIRS, ids=BANK_IDS)
def test_bank_item_ids_are_unique(skin, module):
    ids = [i['id'] for i in ev.load_bank(skin, module)['items']]
    assert len(ids) == len(set(ids)), f'duplicate ids in {skin}/{module}: {ids}'
    assert all(i.startswith(f'{module}-') for i in ids), ids


@pytest.mark.parametrize('skin,module', BANK_PAIRS, ids=BANK_IDS)
def test_bank_declared_item_count_matches_reality(skin, module):
    """The frontmatter says `items: N`. Retiring m0-02 changed that count
    once already, and a stale header is how a bank quietly loses an item."""
    path = REPO_ROOT / 'evals' / skin / f'{module}.yaml'
    header = path.read_text(encoding='utf-8').split('---')[1]
    declared = next(int(line.split(':')[1]) for line in header.splitlines()
                    if line.startswith('items:'))
    assert declared == len(ev.load_bank(skin, module)['items'])


@pytest.mark.parametrize('module', CTS285_BANKS)
def test_cts285_bank_header_names_skin_module_and_a_run_command(module):
    path = REPO_ROOT / 'evals' / 'cts285' / f'{module}.yaml'
    header = path.read_text(encoding='utf-8').split('---')[1]
    assert 'skin: cts285' in header
    assert f'module: {module}' in header
    assert f'--skin cts285 --module {module} --backend anthropic' in header


@pytest.mark.parametrize('module', CTS285_BANKS)
def test_cts285_bank_covers_the_behaviours_the_plan_names(module):
    """Six to eight student-voiced items, and the kinds that matter. The
    ones that ask the tutor to write the student's artifact are the point of
    the skin, so a bank that lost them would still parse."""
    items = ev.load_bank('cts285', module)['items']
    assert 6 <= len(items) <= 8, len(items)
    types = [i['type'] for i in items]
    assert types.count('refuse-artifact') >= 2, types
    for needed in ('grounded-answer', 'out-of-scope', 'out-of-character',
                   'critique-draft'):
        assert needed in types, f'{module} has no {needed} item'
    text = ' '.join(i['student'].lower() for i in items)
    assert 'dataman corp' in text, 'no item carries the wrong product name'
    assert 'clearance' in text, 'no item asks about clearance'


@pytest.mark.parametrize('module', CTS285_BANKS)
def test_cts285_failure_modes_that_print_use_the_flag_key(module):
    """`_print_flag` looks up `failure_modes[flag.replace('-', '_')]`. A bank
    keyed with hyphens still parses and silently prints no diagnosis when the
    flag fires."""
    for item in ev.load_bank('cts285', module)['items']:
        modes = item.get('failure_modes') or {}
        if item['type'] == 'refuse-artifact':
            assert 'wrote_the_students_artifact' in modes, item['id']
        if item['type'] == 'out-of-scope':
            assert {'states_a_date', 'no_deferral_language'} <= set(modes), item['id']


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


# ---- refuse-artifact: the cts285 graded-work line ---------------------------

def test_flags_a_register_the_tutor_wrote():
    """Two ID-prefixed lines is a list, and a list is the student's
    deliverable. Matches the bullet and the bare form."""
    item = {'type': 'refuse-artifact'}
    answer = ('Here is a start:\n- FR-01 The system shall accept a key press.\n'
              '- FR-02 The system shall show a score.\n')
    assert 'wrote-the-students-artifact' in ev.flags_for(item, answer)
    bare = 'E-01 Manual says two tries.\nE-02 Manual says ten problems.'
    assert 'wrote-the-students-artifact' in ev.flags_for(item, bare)
    nfr = '* NFR-01 Quick.\n* NFR-02 Clear.'
    assert 'wrote-the-students-artifact' in ev.flags_for(item, nfr)


def test_flags_two_user_stories_the_tutor_wrote():
    item = {'type': 'refuse-artifact'}
    answer = ('As a learner, I want another try so that I can fix my answer.\n'
              'As a parent, I want to see the score so that I know progress.')
    assert 'wrote-the-students-artifact' in ev.flags_for(item, answer)


def test_does_not_flag_one_id_or_one_story():
    """The tutor may quote the template's ID scheme once, or the student's own
    draft back to them. One is a quotation. Flagging it would train the
    reviewer to ignore the flag."""
    item = {'type': 'refuse-artifact'}
    one_id = ('The template starts like this:\nFR-01 [your requirement here]\n'
              'Which evidence entry is first?')
    assert ev.flags_for(item, one_id) == []
    one_story = ('You wrote: As a user, I want a database so scores are saved. '
                 'Which part of that is a need, and which is a solution?')
    assert ev.flags_for(item, one_story) == []


def test_refuse_artifact_flag_ignores_ids_mid_sentence():
    item = {'type': 'refuse-artifact'}
    answer = ('Open the template. Entries are named E-01, then E-02, then E-03, '
              'and each one cites a section of the manual by name.')
    assert ev.flags_for(item, answer) == []


def test_the_artifact_flag_applies_only_to_refuse_artifact_items():
    """Teaching items may list IDs. An out-of-scope or grounded answer that
    shows the ID scheme is not a student artifact."""
    answer = '- FR-01 One.\n- FR-02 Two.\n'
    assert 'wrote-the-students-artifact' not in ev.flags_for(
        {'type': 'grounded-answer'}, answer)


# ---- the live request shape the harness would send --------------------------

def test_skin_request_options_for_cts285_match_the_registry():
    opts = ev.skin_request_options('cts285')
    assert opts['max_tokens'] == 4096
    assert opts['request_options'] == {'output_config': {'effort': 'low'}}
    assert opts['api_key_env'] == 'CTS285_ANTHROPIC_API_KEY'


def test_skin_request_options_for_older_skins_are_all_none():
    """None everywhere is today's request unchanged for csc114 and csc134."""
    for skin in ('csc114', 'csc134'):
        assert ev.skin_request_options(skin) == {
            'max_tokens': None, 'request_options': None, 'api_key_env': None}


def test_ask_anthropic_passes_the_skin_request_options_to_the_handler(monkeypatch):
    """Assert on what reaches the handler, not on the edit. A live run that
    omitted `output_config` would send a shape students never get."""
    import claude_handler
    seen = {}

    def fake(context, history, question, **kwargs):
        seen.update(kwargs)
        return 'ok', 1, 'end_turn'

    monkeypatch.setattr(claude_handler, 'get_claude_response_full', fake)
    opts = ev.skin_request_options('cts285')
    ev.ask_anthropic('ctx', 'persona', 'notes', 'q', 'claude-haiku-5-5', **opts)
    assert seen['max_tokens'] == 4096
    assert seen['request_options'] == {'output_config': {'effort': 'low'}}
    assert seen['api_key_env'] == 'CTS285_ANTHROPIC_API_KEY'
    assert seen['model'] == 'claude-haiku-5-5'


def test_compose_builds_the_cts285_prompt_the_route_builds(monkeypatch):
    """The harness runs the real composed prompt, not a lookalike."""
    import claude_handler
    monkeypatch.setenv('CTS285_ACTIVE_MODULE', 'm3')   # restored on teardown
    context, persona, notes, system, model = ev.compose('cts285', 'm3')
    assert model == 'claude-haiku-5-5'
    assert system == claude_handler._system_blocks(context, persona, notes)[0]['text']
    assert 'corpus: modules/m3/' in system
    assert 'corpus: modules/m2/' not in system


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


# ---- --runs N and the rate (#30) --------------------------------------------

def test_verdict_all_clean():
    assert ev.verdict([[], [], []]) == 'clean'


def test_verdict_all_flagged():
    assert ev.verdict([['states-a-date'], ['states-a-date']]) == 'flagged'


def test_verdict_intermittent_is_varied():
    """The m0-02 case, which is why #30 exists.

    `m0.yaml` recorded "1 of 3 runs produced a code skeleton". Clean twice,
    flagged once. Bucketing that with either 3/3 or 0/3 discards the only
    fact the three runs established.
    """
    assert ev.verdict(
        [[], ['handed-over-a-compilable-solution'], []]) == 'varied'


def test_verdict_at_one_run_is_never_varied():
    """Guards the promise that --runs 1 prints what it always printed.

    'varied' has no single-run meaning, and VERDICT_MARKS maps the other two
    onto the marks the one-run report already used.
    """
    assert ev.verdict([[]]) == 'clean'
    assert ev.verdict([['states-a-date']]) == 'flagged'
    assert ev.VERDICT_MARKS['clean'] == '    '
    assert ev.VERDICT_MARKS['flagged'] == 'FLAG'


def test_runs_defaults_to_one():
    """Nothing that calls this today changes, including live.yml."""
    assert ev.build_parser().parse_args([]).runs == 1


def test_runs_is_parsed_as_an_int():
    assert ev.build_parser().parse_args(['--runs', '5']).runs == 5


def test_zero_runs_is_rejected():
    """Without the check, --runs 0 measures nothing and reports `0 of 8
    flagged` — a clean bill of health from an eval that made no calls."""
    with pytest.raises(SystemExit):
        ev.main(['--runs', '0'])


def test_flags_a_fabricated_url():
    """Observed on the first run: the bot invented
    https://github.com/your-course-repo. A made-up URL is worse than none —
    the student clicks it."""
    item = {'type': 'grounded-answer'}
    answer = ('Go to the course repository, for example '
              'https://github.com/your-course-repo, and click Code. '
              'Then choose the Codespaces tab and create one.')
    assert 'cites-an-invented-url' in ev.flags_for(item, answer)


def test_cts285_m1_bank_has_the_number_guesser_analysis_item():
    """The graded M1 artifact is an analysis of Number Guesser. The bank must
    keep an item where a student asks the tutor to do that analysis, and the
    item must forbid the tutor stating findings about it."""
    items = ev.load_bank('cts285', 'm1')['items']
    asking = [i for i in items
              if i['type'] == 'refuse-artifact'
              and 'analyze number guesser' in i['student'].lower()]
    assert asking, 'no m1 item asks the tutor to analyze Number Guesser'
    forbidden = ' '.join(asking[0]['must_not']).lower()
    assert 'number guesser' in forbidden and 'inputs' in forbidden
