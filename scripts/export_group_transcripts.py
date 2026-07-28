"""Export one group's conversations and messages to JSON.

Written for K12: once a skin is unregistered, its `/<slug>/admin` route
stops existing and that cohort's rows are unreachable — they stay in
Postgres with no way to read them. Run this *before* repointing a slot,
not after.

    # Against the live database (get the internal connection string from
    # Render; see system1-flask-chat/DEPLOY.md).
    DATABASE_URL=postgres://... python scripts/export_group_transcripts.py csc114

    # Against a local sqlite file
    DATABASE_URL=sqlite:///ta_system.db python scripts/export_group_transcripts.py csc114 -o pilot.json

Read-only: it opens a session, selects, and never writes. Safe to run
against production.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
APP_DIR = REPO_ROOT / 'system1-flask-chat'


def normalize_database_url(url: str) -> str:
    """Match app.py's psycopg3 rewrite so the same URL works in both.

    Render hands out `postgres://`, SQLAlchemy 2 wants an explicit driver,
    and the app pins psycopg3. Duplicated deliberately rather than imported
    — this script must run without building a Flask app, and importing
    app.py would pull in the secrets check.
    """
    if url.startswith('postgres://'):
        return 'postgresql+psycopg://' + url[len('postgres://'):]
    if url.startswith('postgresql://'):
        return 'postgresql+psycopg://' + url[len('postgresql://'):]
    return url


def export_group(session, models, group_name: str) -> dict[str, Any]:
    """Collect one group with its conversations and their messages.

    Ordered by id, not by timestamp: `started_at` and `created_at` are
    server-side defaults with second-ish resolution, so concurrent rows can
    tie. Insertion order is what actually reconstructs a transcript.
    """
    group = session.query(models.Group).filter_by(name=group_name).one_or_none()
    if group is None:
        raise SystemExit(f'no group named {group_name!r} in this database')

    conversations = (session.query(models.Conversation)
                     .filter_by(group_id=group.id)
                     .order_by(models.Conversation.id)
                     .all())

    out_conversations = []
    for conv in conversations:
        messages = (session.query(models.Message)
                    .filter_by(conversation_id=conv.id)
                    .order_by(models.Message.id)
                    .all())
        out_conversations.append({
            'id': conv.id,
            'started_at': conv.started_at.isoformat() if conv.started_at else None,
            'messages': [
                {
                    'id': m.id,
                    'role': m.role,
                    'content': m.content,
                    'tokens_used': m.tokens_used,
                    'created_at': m.created_at.isoformat() if m.created_at else None,
                }
                for m in messages
            ],
        })

    return {
        'group': {
            'id': group.id,
            'name': group.name,
            'clearance_level': group.clearance_level,
            'token_budget': group.token_budget,
            'tokens_used': group.tokens_used,
            'created_at': group.created_at.isoformat() if group.created_at else None,
        },
        # These counts are the point of the file, not decoration: a cohort
        # shared one Group row and one conversation chain, so an export that
        # looks thin is evidence about the interleaving bug rather than a
        # failed export.
        'conversation_count': len(out_conversations),
        'message_count': sum(len(c['messages']) for c in out_conversations),
        'conversations': out_conversations,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('group', help="group name, which is the skin slug (e.g. 'csc114')")
    p.add_argument('-o', '--output', help='write here instead of stdout')
    args = p.parse_args(argv)

    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise SystemExit(
            'DATABASE_URL is not set. For the live database use the *internal* '
            'connection string — the external one needs a TLS handshake that '
            'flakes from inside Render. See system1-flask-chat/DEPLOY.md.'
        )

    sys.path.insert(0, str(APP_DIR))
    import models

    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    engine = create_engine(normalize_database_url(database_url))
    with Session(engine) as session:
        payload = export_group(session, models, args.group)

    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(text + '\n', encoding='utf-8')
        print(f'wrote {args.output}: {payload["conversation_count"]} conversations, '
              f'{payload["message_count"]} messages')
    else:
        print(text)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
