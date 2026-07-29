"""Tests for the K12 transcript export.

This script runs once, against production, on data that becomes
unreachable immediately afterwards. There is no second attempt and no way
to check the result against the source, so it is tested against a real
sqlite database rather than mocks.
"""
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / 'system1-flask-chat'))

from scripts.export_group_transcripts import (  # noqa: E402
    export_group, main, normalize_database_url,
)


@pytest.fixture
def session(tmp_path):
    """A real sqlite database with the app's schema and two cohorts in it."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    import models

    engine = create_engine(f'sqlite:///{tmp_path / "t.db"}')
    models.db.Model.metadata.create_all(engine)

    with Session(engine) as s:
        keep = models.Group(name='csc114', clearance_level='ORANGE')
        other = models.Group(name='csc134', clearance_level='ORANGE')
        s.add_all([keep, other])
        s.flush()

        c1 = models.Conversation(group_id=keep.id)
        c2 = models.Conversation(group_id=keep.id)
        c3 = models.Conversation(group_id=other.id)
        s.add_all([c1, c2, c3])
        s.flush()

        s.add_all([
            models.Message(conversation_id=c1.id, role='user',
                           content='how do i start', tokens_used=0),
            models.Message(conversation_id=c1.id, role='assistant',
                           content='What have you tried?', tokens_used=7200),
            models.Message(conversation_id=c2.id, role='user',
                           content='second conversation', tokens_used=0),
            models.Message(conversation_id=c3.id, role='user',
                           content='belongs to csc134', tokens_used=0),
        ])
        s.commit()
        yield s, models


# ---- URL handling ---------------------------------------------------------
#
# Must match app.py, or the script works locally and fails against Render.

@pytest.mark.parametrize('given,expected', [
    ('postgres://u:p@h/db', 'postgresql+psycopg://u:p@h/db'),
    ('postgresql://u:p@h/db', 'postgresql+psycopg://u:p@h/db'),
    ('postgresql+psycopg://u:p@h/db', 'postgresql+psycopg://u:p@h/db'),
    ('sqlite:///ta_system.db', 'sqlite:///ta_system.db'),
])
def test_normalize_database_url(given, expected):
    assert normalize_database_url(given) == expected


# ---- export ---------------------------------------------------------------

def test_export_collects_the_groups_conversations_and_messages(session):
    s, models = session
    out = export_group(s, models, 'csc114')

    assert out['group']['name'] == 'csc114'
    assert out['conversation_count'] == 2
    assert out['message_count'] == 3

    first = out['conversations'][0]
    assert [m['role'] for m in first['messages']] == ['user', 'assistant']
    assert first['messages'][0]['content'] == 'how do i start'
    assert first['messages'][1]['tokens_used'] == 7200


def test_export_does_not_leak_another_cohorts_messages(session):
    """The groups share tables; an export keyed on the wrong column would
    quietly hand one cohort's transcripts to another."""
    s, models = session
    out = export_group(s, models, 'csc114')

    bodies = [m['content'] for c in out['conversations'] for m in c['messages']]
    assert 'belongs to csc134' not in bodies


def test_export_is_json_serialisable(session):
    """Datetimes must already be strings — this is written straight to a file."""
    s, models = session
    json.dumps(export_group(s, models, 'csc114'))


def test_missing_group_exits_rather_than_writing_an_empty_export(session):
    """An empty JSON file would read as 'the pilot had no traffic' — the one
    wrong answer that looks like a successful run."""
    s, models = session
    with pytest.raises(SystemExit):
        export_group(s, models, 'nonexistent')


# ---- CLI ------------------------------------------------------------------

def test_main_refuses_to_run_without_a_database_url(monkeypatch):
    monkeypatch.delenv('DATABASE_URL', raising=False)
    with pytest.raises(SystemExit) as excinfo:
        main(['csc114'])
    assert 'DATABASE_URL' in str(excinfo.value)


def test_main_writes_a_file(tmp_path, monkeypatch, session):
    s, models = session
    db_path = s.get_bind().url.database
    monkeypatch.setenv('DATABASE_URL', f'sqlite:///{db_path}')

    out = tmp_path / 'pilot.json'
    assert main(['csc114', '-o', str(out)]) == 0

    payload = json.loads(out.read_text(encoding='utf-8'))
    assert payload['message_count'] == 3
