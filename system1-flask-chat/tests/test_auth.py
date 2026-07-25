# tests/test_auth.py
import pytest
from auth import (
    SKINS,
    authenticate_skin,
    load_skin_context,
    # compat aliases (deleted in T8)
    GROUPS,
    authenticate_group,
    load_group_context,
)


# ---- new-contract (SKINS) --------------------------------------------------

def test_csc114_skin_present():
    assert 'csc114' in SKINS
    assert SKINS['csc114']['password'] == '2026su'
    assert SKINS['csc114']['clearance'] == 'ORANGE'
    assert SKINS['csc114']['model'] == 'claude-sonnet-4-6'


def test_csc134_skin_present_on_haiku():
    assert 'csc134' in SKINS
    assert SKINS['csc134']['model'] == 'claude-haiku-4-5-20251001'
    assert SKINS['csc134']['password']  # must be set (placeholder OK)


def test_authenticate_skin_valid():
    s = authenticate_skin('csc114', '2026su')
    assert s is not None
    assert s['model'] == 'claude-sonnet-4-6'


def test_authenticate_skin_bad_password():
    assert authenticate_skin('csc114', 'wrong') is None


def test_authenticate_skin_unknown_slug():
    assert authenticate_skin('nope', '2026su') is None


def test_load_skin_context_returns_header(tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# CSC 114 header')
    out = load_skin_context('csc114')
    assert '# CSC 114 header' in out


def test_load_skin_context_appends_corpus(tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# header')
    corpus = tmp_path / 'csc114'
    corpus.mkdir()
    (corpus / 'week-01.md').write_text('# week 1 body')
    out = load_skin_context('csc114')
    assert '# header' in out
    assert '--- corpus: week-01.md ---' in out
    assert '# week 1 body' in out


def test_load_skin_context_missing_header_raises(tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    with pytest.raises(FileNotFoundError):
        load_skin_context('csc114')


def test_load_skin_context_unknown_slug_raises():
    with pytest.raises(KeyError):
        load_skin_context('bogus')


# ---- compat aliases (removed in T8) ---------------------------------------

def test_compat_authenticate_group_still_works():
    g = authenticate_group('csc114', '2026su')
    assert g is not None
    assert g['clearance'] == 'ORANGE'


def test_compat_load_group_context_csc114(tmp_path, monkeypatch):
    import auth
    monkeypatch.setattr(auth, 'CONTEXT_DIR', tmp_path)
    (tmp_path / 'csc114_context.md').write_text('# CSC 114')
    result = load_group_context('csc114')
    assert '# CSC 114' in result


def test_compat_groups_keyset_unchanged():
    # csc134 is deliberately absent from the compat map — it uses SKINS.
    assert set(GROUPS.keys()) == {'csc114', 'group2', 'group3', 'group4', 'group5'}
