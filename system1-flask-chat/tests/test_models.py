import pytest
from models import Group, Conversation, Message

def test_group_defaults(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='group1', clearance_level='ORANGE')
        db.session.add(g)
        db.session.commit()
        assert g.token_budget == 100000
        assert g.tokens_used == 0

def test_conversation_linked_to_group(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='group2', clearance_level='YELLOW')
        db.session.add(g)
        db.session.commit()
        c = Conversation(group_id=g.id)
        db.session.add(c)
        db.session.commit()
        assert c.group_id == g.id

def test_message_linked_to_conversation(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='group3', clearance_level='ORANGE')
        db.session.add(g)
        db.session.commit()
        c = Conversation(group_id=g.id)
        db.session.add(c)
        db.session.commit()
        m = Message(conversation_id=c.id, role='user', content='Hello', tokens_used=5)
        db.session.add(m)
        db.session.commit()
        assert m.role == 'user'
        assert m.tokens_used == 5

def test_group_increment_tokens(app):
    with app.app_context():
        from models import db
        db.create_all()
        g = Group(name='group4', clearance_level='ORANGE')
        db.session.add(g)
        db.session.commit()
        g.increment_tokens(500)
        db.session.commit()
        assert g.tokens_used == 500
        assert g.tokens_remaining == 99500
