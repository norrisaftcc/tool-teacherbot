"""Migrations must describe the models, and must not fight create_all.

K6 was frozen as "no schema change to an existing table until Alembic
lands" because nothing could *detect* the mistake: `create_all()` ignores a
new column silently, and the suite runs on in-memory SQLite where the
schema is rebuilt from the models every run, so a missing migration is
invisible until production raises UndefinedColumn. ADR-0006 supersedes that
prohibition, and these tests are what replaces it.
"""
from pathlib import Path

import pytest
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from flask_migrate import upgrade
from sqlalchemy import create_engine, inspect

from app import create_app
from models import db

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / 'migrations'


@pytest.fixture
def migrated_app(tmp_path):
    """An app on a real file-backed database with migrations applied.

    TESTING is False on purpose: create_app only calls create_all under
    TESTING, and letting it run here would build the tables before Alembic
    could, so `upgrade` would fail on tables that "already exist" — which is
    exactly the collision this file exists to rule out.

    File-backed rather than :memory: because Alembic opens its own
    connection, and an in-memory database is per-connection.
    """
    app = create_app({
        'TESTING': False,
        'SECRET_KEY': 'test-secret',
        'ADMIN_PASSWORD': 'testadmin',
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{tmp_path / "m.db"}',
    })
    with app.app_context():
        upgrade(directory=str(MIGRATIONS_DIR))
        yield app


def test_migrations_build_the_expected_schema(migrated_app):
    tables = set(inspect(db.engine).get_table_names())
    assert {'groups', 'conversations', 'messages'} <= tables
    # Alembic's bookkeeping table — its absence means the migration ran as
    # raw DDL and the revision was never recorded.
    assert 'alembic_version' in tables


def test_models_and_migrations_do_not_drift(migrated_app):
    """The check that lets ADR-0004 add tables without a production gamble.

    Fails when models.py declares something no migration creates — a new
    column, a widened type, a dropped constraint. That is the failure that
    used to reach production silently, because the model is the only thing
    tests build from.
    """
    with db.engine.connect() as connection:
        context = MigrationContext.configure(connection)
        diff = compare_metadata(context, db.metadata)

    assert diff == [], (
        'models.py and migrations/ disagree. Run:\n'
        '    cd system1-flask-chat && flask db migrate -m "<what changed>"\n'
        f'Outstanding differences: {diff}'
    )


def test_downgrade_is_reversible(migrated_app):
    """A migration you cannot roll back is a migration you cannot deploy."""
    from flask_migrate import downgrade

    downgrade(directory=str(MIGRATIONS_DIR))
    after = set(inspect(db.engine).get_table_names())
    assert 'groups' not in after
    assert 'messages' not in after

    upgrade(directory=str(MIGRATIONS_DIR))
    assert 'groups' in set(inspect(db.engine).get_table_names())


# ---- the create_all guard -------------------------------------------------

def test_create_all_does_not_run_outside_testing(tmp_path):
    """Production schema belongs to Alembic alone.

    If create_app built tables at boot, they would carry no alembic_version
    row — invisible to Alembic, which would then try to create them again on
    the next migration and fail the deploy on a table that already exists.
    """
    db_path = tmp_path / 'untouched.db'
    create_app({
        'TESTING': False,
        'SECRET_KEY': 'test-secret',
        'ADMIN_PASSWORD': 'testadmin',
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
    })

    if db_path.exists():
        assert inspect(create_engine(f'sqlite:///{db_path}')).get_table_names() == []


def test_create_all_still_runs_under_testing(tmp_path):
    """...but the suite depends on it: conftest never calls create_all."""
    db_path = tmp_path / 'built.db'
    create_app({
        'TESTING': True,
        'SECRET_KEY': 'test-secret',
        'ADMIN_PASSWORD': 'testadmin',
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
    })

    assert 'groups' in set(inspect(create_engine(f'sqlite:///{db_path}')).get_table_names())
