import json
from flask import Blueprint, render_template, redirect, url_for, session, request, flash, jsonify, current_app, Response, stream_with_context
from functools import wraps
from claude_handler import get_claude_response, stream_claude_response

main = Blueprint('main', __name__)


def group_login_required(f):
    """Session-based auth check for group login."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'group_id' not in session:
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
    if request.method == 'POST':
        from auth import authenticate_group, load_group_context
        from models import db, Group

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

        # Ensure Group row exists in DB
        group = Group.query.filter_by(name=group_id).first()
        if not group:
            group = Group(name=group_id, clearance_level=group_data['clearance'])
            db.session.add(group)
            db.session.commit()

        return redirect(url_for('main.chat'))

    return render_template('login.html')


@main.route('/chat')
@group_login_required
def chat():
    return render_template('chat.html',
                           group_id=session.get('group_id', ''),
                           clearance=session.get('clearance', ''))


@main.route('/api/chat', methods=['POST'])
@group_login_required
def api_chat():
    from models import db, Group, Conversation, Message

    data = request.get_json()
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
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 502

    # Log to DB — failures here must not block the response
    try:
        if group:
            conv = (Conversation.query
                    .filter_by(group_id=group.id)
                    .order_by(Conversation.started_at.desc())
                    .first())
            if not conv or not history:
                conv = Conversation(group_id=group.id)
                db.session.add(conv)
                db.session.flush()

            db.session.add(Message(conversation_id=conv.id, role='user',
                                   content=user_message, tokens_used=0))
            db.session.add(Message(conversation_id=conv.id, role='assistant',
                                   content=response_text, tokens_used=tokens_used))
            group.increment_tokens(tokens_used)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'DB write failed for {session["group_id"]}: {e}')

    return jsonify({
        'response': response_text,
        'tokens_remaining': group.tokens_remaining if group else None,
    })


@main.route('/api/chat/stream', methods=['POST'])
@group_login_required
def api_chat_stream():
    from models import db, Group, Conversation, Message

    data = request.get_json()
    user_message = (data.get('message') or '').strip()
    history = data.get('history') or []

    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    group = Group.query.filter_by(name=session['group_id']).first()
    if group and group.tokens_remaining <= 0:
        return jsonify({'error': 'Token budget exhausted. Contact your instructor.'}), 403

    group_context = session['group_context']
    group_id = session['group_id']

    def generate():
        full_text = ''
        total_tokens = 0
        try:
            for chunk, tokens in stream_claude_response(group_context, history, user_message):
                if chunk:
                    full_text += chunk
                    yield f'data: {json.dumps({"chunk": chunk})}\n\n'
                elif tokens:
                    total_tokens = tokens
        except RuntimeError as e:
            yield f'data: {json.dumps({"error": str(e)})}\n\n'
            return

        # Log to DB after streaming completes — failure must not surface to client
        try:
            g = Group.query.filter_by(name=group_id).first()
            if g:
                conv = (Conversation.query
                        .filter_by(group_id=g.id)
                        .order_by(Conversation.started_at.desc())
                        .first())
                if not conv or not history:
                    conv = Conversation(group_id=g.id)
                    db.session.add(conv)
                    db.session.flush()
                db.session.add(Message(conversation_id=conv.id, role='user',
                                       content=user_message, tokens_used=0))
                db.session.add(Message(conversation_id=conv.id, role='assistant',
                                       content=full_text, tokens_used=total_tokens))
                g.increment_tokens(total_tokens)
                db.session.commit()
                remaining = g.tokens_remaining
            else:
                remaining = None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'DB write failed for {group_id}: {e}')
            remaining = None

        yield f'data: {json.dumps({"done": True, "tokens_remaining": remaining})}\n\n'

    return Response(stream_with_context(generate()), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


@main.route('/admin')
def admin():
    password = request.args.get('password', '')
    if password != current_app.config.get('ADMIN_PASSWORD', ''):
        return render_template('admin_login.html'), 200

    from models import Group, Conversation, Message
    groups = Group.query.all()
    conversations = (Conversation.query
                     .order_by(Conversation.started_at.desc())
                     .limit(50)
                     .all())
    return render_template('admin.html', groups=groups, conversations=conversations)


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
