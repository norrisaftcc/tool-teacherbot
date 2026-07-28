import json
from functools import wraps

from flask import (
    Blueprint, render_template, redirect, url_for, session, request,
    flash, jsonify, current_app, Response, stream_with_context,
)

from claude_handler import get_claude_response, stream_claude_response


# ---------------------------------------------------------------------------
# Global blueprint: picker + logout. Registered at the root of the app.
# ---------------------------------------------------------------------------

main = Blueprint('main', __name__)


@main.route('/')
def index():
    from auth import SKINS
    active_slug = session.get('skin')
    return render_template('picker.html', skins=SKINS, active_slug=active_slug)


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


# ---------------------------------------------------------------------------
# Skin blueprint factory: one instance per SKIN, registered at /<slug>.
# ---------------------------------------------------------------------------

def skin_login_required(slug: str):
    """Gate a skin-scoped route: HTML routes 302 to this skin's login,
    JSON API routes return 401 (so chat.js sees an error instead of an
    opaque redirect followed by an HTML body)."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get('skin') != slug:
                if '/api/' in request.path:
                    return jsonify({'error': 'Not authenticated for this skin.'}), 401
                return redirect(url_for(f'skin_{slug}.login_view'))
            return f(*args, **kwargs)
        return decorated
    return decorator


def skin_blueprint(slug: str) -> Blueprint:
    """Build a Blueprint that serves the /{slug}/… surface for one skin."""
    from auth import SKINS
    bp = Blueprint(f'skin_{slug}', __name__)
    require_login = skin_login_required(slug)

    def _skin() -> dict:
        # Fetched fresh so a running app can be reloaded without stale copies.
        return SKINS[slug]

    def _login_action() -> str:
        return url_for(f'skin_{slug}.do_login')

    def _admin_action() -> str:
        return url_for(f'skin_{slug}.admin')

    @bp.route('/', endpoint='login_view')
    def login_view():
        skin = _skin()
        return render_template(
            'login.html',
            slug=slug,
            skin=skin,
            login_action=_login_action(),
        )

    @bp.route('/login', methods=['POST'], endpoint='do_login')
    def do_login():
        from auth import (authenticate_skin, load_skin_context, load_skin_notes,
                          load_skin_persona)
        from models import db, Group

        password = (request.form.get('password') or '').strip()
        skin_entry = authenticate_skin(slug, password)
        if not skin_entry:
            flash('Invalid passcode for this cohort.')
            return render_template(
                'login.html',
                slug=slug,
                skin=SKINS[slug],
                login_action=_login_action(),
            ), 200

        # Validate the persona and cohort header/corpus load now so we
        # surface any FileNotFoundError before the user reaches /chat. We
        # do NOT cache either in the session — see api_chat /
        # api_chat_stream, which reload them per request. (The windowed
        # corpus is tens of KB and would blow past the 4KB signed-cookie
        # limit if we stored it.)
        try:
            load_skin_persona(slug)
            load_skin_notes(slug)
            load_skin_context(slug)
        except FileNotFoundError as e:
            flash(str(e))
            return render_template(
                'login.html',
                slug=slug,
                skin=SKINS[slug],
                login_action=_login_action(),
            ), 200

        session.clear()
        session['skin'] = slug
        session['clearance'] = skin_entry['clearance']

        group = Group.query.filter_by(name=slug).first()
        if not group:
            group = Group(name=slug, clearance_level=skin_entry['clearance'])
            db.session.add(group)
            db.session.commit()
        elif group.raise_budget_floor():
            # Existing rows predate the budget resize and cannot be fixed by
            # the column default — see Group.raise_budget_floor.
            db.session.commit()

        return redirect(url_for(f'skin_{slug}.chat'))

    @bp.route('/chat', endpoint='chat')
    @require_login
    def chat():
        skin = _skin()
        return render_template(
            'chat.html',
            slug=slug,
            skin=skin,
            clearance=session.get('clearance', skin['clearance']),
        )

    @bp.route('/api/chat', methods=['POST'], endpoint='api_chat')
    @require_login
    def api_chat():
        from auth import load_skin_context, load_skin_notes, load_skin_persona
        from models import db, Group, Conversation, Message

        data = request.get_json(silent=True) or {}
        user_message = (data.get('message') or '').strip()
        history = data.get('history') or []

        if not user_message:
            return jsonify({'error': 'Empty message'}), 400

        skin = _skin()
        group = Group.query.filter_by(name=slug).first()
        if group and group.tokens_remaining <= 0:
            return jsonify({'error': 'Token budget exhausted. Contact your instructor.'}), 403

        try:
            response_text, tokens_used = get_claude_response(
                load_skin_context(slug), history, user_message,
                model=skin['model'], persona=load_skin_persona(slug),
                notes=load_skin_notes(slug),
            )
        except RuntimeError as e:
            return jsonify({'error': str(e)}), 502

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
            current_app.logger.error(f'DB write failed for {slug}: {e}')

        return jsonify({
            'response': response_text,
            'tokens_remaining': group.tokens_remaining if group else None,
        })

    @bp.route('/api/chat/stream', methods=['POST'], endpoint='api_chat_stream')
    @require_login
    def api_chat_stream():
        from auth import load_skin_context, load_skin_notes, load_skin_persona
        from models import db, Group, Conversation, Message

        data = request.get_json(silent=True) or {}
        user_message = (data.get('message') or '').strip()
        history = data.get('history') or []

        if not user_message:
            return jsonify({'error': 'Empty message'}), 400

        skin = _skin()
        group = Group.query.filter_by(name=slug).first()
        if group and group.tokens_remaining <= 0:
            return jsonify({'error': 'Token budget exhausted. Contact your instructor.'}), 403

        # Read both outside generate() — the generator body runs after the
        # request context is torn down.
        skin_context = load_skin_context(slug)
        skin_persona = load_skin_persona(slug)
        skin_notes = load_skin_notes(slug)
        model = skin['model']

        def generate():
            full_text = ''
            total_tokens = 0
            try:
                for chunk, tokens in stream_claude_response(
                    skin_context, history, user_message,
                    model=model, persona=skin_persona, notes=skin_notes,
                ):
                    if chunk:
                        full_text += chunk
                        yield f'data: {json.dumps({"chunk": chunk})}\n\n'
                    elif tokens:
                        total_tokens = tokens
            except RuntimeError as e:
                yield f'data: {json.dumps({"error": str(e)})}\n\n'
                return

            try:
                g = Group.query.filter_by(name=slug).first()
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
                current_app.logger.error(f'DB write failed for {slug}: {e}')
                remaining = None

            yield f'data: {json.dumps({"done": True, "tokens_remaining": remaining})}\n\n'

        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'},
        )

    @bp.route('/admin', endpoint='admin')
    def admin():
        from models import Group, Conversation
        password = request.args.get('password', '')
        if password != current_app.config.get('ADMIN_PASSWORD', ''):
            return render_template(
                'admin_login.html',
                slug=slug,
                skin=SKINS[slug],
                admin_action=_admin_action(),
            ), 200

        group = Group.query.filter_by(name=slug).first()
        groups = [group] if group else []
        conversations = []
        if group:
            conversations = (Conversation.query
                             .filter_by(group_id=group.id)
                             .order_by(Conversation.started_at.desc())
                             .limit(50)
                             .all())
        return render_template(
            'admin.html',
            slug=slug,
            skin=SKINS[slug],
            groups=groups,
            conversations=conversations,
        )

    return bp
