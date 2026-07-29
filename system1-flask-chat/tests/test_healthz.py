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
import logging
from unittest.mock import patch

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


SECRETS = ('hunter2', 'dpg-secret-host', 'postgresql+psycopg')


def _dsn_bearing_failure():
    """An OperationalError that renders the connection it failed on.

    psycopg does exactly this, which is the whole problem: `str(e)` on a
    connection failure contains user, password and host.
    """
    return OperationalError(
        'SELECT 1', {},
        Exception('could not connect to postgresql+psycopg://'
                  'teacherbot:hunter2@dpg-secret-host/teacherbot'),
    )


def test_healthz_does_not_leak_the_connection_string(client):
    """A 503 body is public. It must not carry host, user, or password."""
    from models import db

    with patch.object(db.session, 'execute', side_effect=_dsn_bearing_failure()):
        r = client.get('/healthz')

    body = r.get_data(as_text=True)
    for secret in SECRETS:
        assert secret not in body


def test_healthz_does_not_leak_the_connection_string_into_logs(client, caplog):
    """The half I missed the first time.

    The original version asserted the DSN stayed out of the response body
    and then interpolated the exception straight into `logger.error`. Logs
    are shipped to third parties as a matter of course, so that is the same
    leak through a quieter hole. Only the exception type is logged now.
    """
    from models import db

    with caplog.at_level(logging.ERROR):
        with patch.object(db.session, 'execute',
                          side_effect=_dsn_bearing_failure()):
            client.get('/healthz')

    logged = '\n'.join(r.getMessage() for r in caplog.records)
    assert logged, 'the failure was not logged at all — it must be'
    for secret in SECRETS:
        assert secret not in logged
    # Still useful: the type distinguishes DNS failure from auth rejection.
    assert 'OperationalError' in logged


def test_healthz_rolls_back_the_failed_session(client):
    """A failed execute poisons the request-scoped session.

    Without the rollback, anything later in the same request raises
    InvalidRequestError and the real cause is buried.
    """
    from models import db

    with patch.object(db.session, 'execute',
                      side_effect=_dsn_bearing_failure()):
        with patch.object(db.session, 'rollback') as rollback:
            client.get('/healthz')

    rollback.assert_called_once()


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
