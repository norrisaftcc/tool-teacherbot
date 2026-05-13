from functools import wraps
from flask import (
    Blueprint, render_template, redirect, url_for, request, session, flash,
    current_app, jsonify,
)

from auth import authenticate_group, load_group_context
from models import db, Group, Conversation, Message

main = Blueprint('main', __name__)


def group_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'group_id' not in session:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Not authenticated'}), 401
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated


@main.route('/')
def index():
    if 'group_id' in session:
        return redirect(url_for('main.chat'))
    return render_template('login.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    group_id = request.form.get('group_id', '').strip()
    password = request.form.get('password', '').strip()

    group_data = authenticate_group(group_id, password)
    if not group_data:
        flash('Invalid group ID or password.')
        return render_template('login.html'), 200

    try:
        context = load_group_context(group_id)
    except FileNotFoundError as e:
        flash(str(e))
        return render_template('login.html'), 200

    session['group_id'] = group_id
    session['group_context'] = context
    session['clearance'] = group_data['clearance']

    group = Group.query.filter_by(name=group_id).first()
    if not group:
        group = Group(name=group_id, clearance_level=group_data['clearance'])
        db.session.add(group)
        db.session.commit()

    return redirect(url_for('main.chat'))


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


@main.route('/chat')
@group_login_required
def chat():
    group = Group.query.filter_by(name=session['group_id']).first()
    return render_template(
        'chat.html',
        group_id=session['group_id'],
        clearance=session.get('clearance', ''),
        tokens_remaining=group.tokens_remaining if group else None,
        token_budget=group.token_budget if group else None,
    )


@main.route('/api/chat', methods=['POST'])
@group_login_required
def api_chat():
    from claude_handler import get_claude_response

    data = request.get_json(silent=True) or {}
    user_message = (data.get('message') or '').strip()
    history = data.get('history') or []

    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    group = Group.query.filter_by(name=session['group_id']).first()
    if group and group.tokens_remaining <= 0:
        return jsonify({'error': 'Token budget exhausted. Contact your instructor.'}), 403

    try:
        response_text, tokens_used = get_claude_response(
            session['group_context'], history, user_message
        )
    except Exception as e:
        return jsonify({'error': f'Claude API error: {e}'}), 502

    try:
        conv = (
            Conversation.query.filter_by(group_id=group.id)
            .order_by(Conversation.started_at.desc())
            .first()
        )
        if not conv or len(history) == 0:
            conv = Conversation(group_id=group.id)
            db.session.add(conv)
            db.session.flush()

        db.session.add(Message(
            conversation_id=conv.id, role='user',
            content=user_message, tokens_used=0,
        ))
        db.session.add(Message(
            conversation_id=conv.id, role='assistant',
            content=response_text, tokens_used=tokens_used,
        ))
        group.increment_tokens(tokens_used)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.warning('DB write failed: %s', e)

    return jsonify({
        'response': response_text,
        'tokens_remaining': group.tokens_remaining if group else None,
    })


@main.route('/admin', methods=['GET', 'POST'])
def admin():
    password = request.values.get('password', '')
    if password != current_app.config.get('ADMIN_PASSWORD', ''):
        return render_template('admin_login.html'), 200

    groups = Group.query.order_by(Group.name).all()
    conversations = (
        Conversation.query.order_by(Conversation.started_at.desc()).limit(50).all()
    )
    return render_template(
        'admin.html',
        groups=groups,
        conversations=conversations,
        admin_password=password,
    )
