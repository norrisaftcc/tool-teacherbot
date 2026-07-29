"""The healthcheck must fail when the database is unreachable.

Written against a real incident (#38): on 2026-07-29 the production
database was deleted by free-tier expiry, `db.create_all()` had just
stopped running at boot (ADR-0006), and the service came up "live" serving
the cohort picker while every login 500'd. Render's health check polled a
route that never touches Postgres, saw 200, and reported the service
healthy.

The test that matters here is the 503 one. A healthcheck that only ever
returns 200 in tests is the same non-signal as the one it replaced.
"""
from unittest.mock import patch

import pytest
from sqlalchemy.exc import OperationalError


def test_healthz_reports_ok_when_the_database_answers(client):
    r = client.get('/healthz')
    assert r.status_code == 200
    assert r.get_json() == {'status': 'ok', 'database': 'ok'}


def test_healthz_returns_503_when_the_database_is_unreachable(client, app):
    """The case the old healthcheck could not see.

    Simulates the observed failure: `failed to resolve host
    'dpg-d84h9epkh4rs73d70pgg-a'` — name resolution, i.e. the instance is
    gone, not merely refusing connections.
    """
    from models import db

    boom = OperationalError(
        'SELECT 1', {},
        Exception("failed to resolve host 'dpg-d84h9epkh4rs73d70pgg-a'"),
    )
    with patch.object(db.session, 'execute', side_effect=boom):
        r = client.get('/healthz')

    assert r.status_code == 503
    assert r.get_json()['database'] == 'unreachable'


def test_healthz_does_not_leak_the_connection_string(client):
    """A 503 body is public. It must not carry host, user, or password."""
    from models import db

    boom = OperationalError(
        'SELECT 1', {},
        Exception('could not connect to postgresql+psycopg://'
                  'teacherbot:hunter2@dpg-secret-host/teacherbot'),
    )
    with patch.object(db.session, 'execute', side_effect=boom):
        r = client.get('/healthz')

    body = r.get_data(as_text=True)
    for secret in ('hunter2', 'dpg-secret-host', 'postgresql+psycopg'):
        assert secret not in body


def test_healthz_needs_no_login(client):
    """Render polls it unauthenticated; a redirect would read as unhealthy."""
    r = client.get('/healthz')
    assert r.status_code == 200


def test_picker_still_answers_without_touching_the_database(client, app):
    """Pins the asymmetry that caused #38, so the reasoning survives.

    `/` must keep working from the SKINS dict alone — that is what makes it
    useless as a health signal, and why /healthz exists.
    """
    from models import db

    boom = OperationalError('SELECT 1', {}, Exception('gone'))
    with patch.object(db.session, 'execute', side_effect=boom):
        assert client.get('/').status_code == 200
        assert client.get('/healthz').status_code == 503
