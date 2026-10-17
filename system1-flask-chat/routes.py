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


@main.route('/healthz')
def healthz():
    """Liveness that actually touches Postgres. Render's health check path.

    `/` renders the picker straight from the in-memory SKINS dict and never
    queries anything, so it returns 200 over a database that does not
    exist. That is not hypothetical: on 2026-07-29 the free-tier database
    was deleted by its 30-day expiry, `db.create_all()` had just stopped
    running at boot (ADR-0006), and the service came up "live" serving a
    cohort picker while every login 500'd. Render's health check saw 200
    and agreed. See #38.

    So this executes a real query. A deploy whose DATABASE_URL is wrong, or
    whose preDeployCommand migration failed, now fails its health check
    instead of going live broken.

    Neither the response body nor the log carries the exception text. A
    psycopg OperationalError renders the connection it failed on, so `{e}`
    can contain the full DSN — user, password, host. The 503 body is public
    and logs are routinely shipped to third parties, so only the exception
    *type* is recorded. That is enough to tell a DNS failure from an auth
    rejection, which is all this endpoint needs to say.
    """
    from sqlalchemy import text
    from models import db

    try:
        db.session.execute(text('SELECT 1'))
    except Exception as e:
        current_app.logger.error(
            'healthz: database unreachable (%s)', type(e).__name__)
        # A failed execute leaves the session in a broken transaction, and
        # the session is request-scoped — without this, anything later in
        # the same request fails with InvalidRequestError instead of the
        # real cause.
        db.session.rollback()
        return jsonify({'status': 'error', 'database': 'unreachable'}), 503
    return jsonify({'status': 'ok', 'database': 'ok'}), 200


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


NEUTRAL_API_ERROR = 'The tutor is unavailable right now. Try again later, or ask your instructor.'


def _clamp_history(history, limit: int) -> list[dict]:
    """The last ``limit`` well-formed history items.

    The client supplies history, so every item is untrusted: only dicts with
    a user/assistant role and string content survive. A leading assistant
    turn is dropped after the cut, because slicing an arbitrary window can
    start on one and a conversation should open on the student.

    This bounds cost, not forgery — a client can still claim the assistant
    said anything inside the window (ADR-0004 context).
    """
    if not isinstance(history, list):
        return []
    clean = [
        {'role': item['role'], 'content': item['content']}
        for item in history
        if isinstance(item, dict)
        and item.get('role') in ('user', 'assistant')
        and isinstance(item.get('content'), str)
    ]
    clean = clean[-limit:] if limit > 0 else []
    while clean and clean[0]['role'] != 'user':
        clean.pop(0)
    return clean


def _read_chat_request(skin: dict):
    """Parse and bound a chat POST.

    Returns ``(user_message, history, error_response)``; exactly one of the
    tail pair is None. Skins that declare no caps get today's behaviour:
    history passes through untouched.
    """
    data = request.get_json(silent=True) or {}
    raw = data.get('message')
    user_message = raw.strip() if isinstance(raw, str) else ''
    history = data.get('history') or []

    if not user_message:
        return None, None, (jsonify({'error': 'Empty message'}), 400)

    max_chars = skin.get('max_message_chars')
    if max_chars and len(user_message) > max_chars:
        return None, None, (jsonify({
            'error': f'Message too long. Keep it under {max_chars:,} characters.',
        }), 400)

    limit = skin.get('history_messages')
    if limit is not None:
        history = _clamp_history(history, limit)
    return user_message, history, None


def _api_options(skin: dict) -> dict:
    """Per-skin kwargs for claude_handler. Empty for a skin that sets none."""
    return {
        'max_tokens': skin.get('max_tokens'),
        'request_options': skin.get('request_options'),
        'api_key_env': skin.get('api_key_env'),
    }


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
        username = request.form.get('username') or ''
        skin_entry = authenticate_skin(slug, password, username)
        if not skin_entry:
            flash('Invalid username or password.' if SKINS[slug].get('username')
                  else 'Invalid passcode for this cohort.')
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
            if skin_entry.get('token_budget'):
                # A skin's own budget; the column default is the global one.
                group.token_budget = skin_entry['token_budget']
            db.session.add(group)
            db.session.commit()
        elif group.raise_budget_floor(skin_entry.get('token_budget')):
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

        skin = _skin()
        user_message, history, error = _read_chat_request(skin)
        if error:
            return error

        group = Group.query.filter_by(name=slug).first()
        if group and group.tokens_remaining <= 0:
            return jsonify({'error': 'Token budget exhausted. Contact your instructor.'}), 403

        try:
            response_text, tokens_used = get_claude_response(
                load_skin_context(slug), history, user_message,
                model=skin['model'], persona=load_skin_persona(slug),
                notes=load_skin_notes(slug), **_api_options(skin),
            )
        except RuntimeError as e:
            if skin.get('chrome') == 'neutral':
                # The SDK message can carry request detail; a student does not
                # need it and the log only needs the type.
                current_app.logger.error(
                    'Claude API error for %s (%s)', slug, type((e.__cause__ or e)).__name__)
                return jsonify({'error': NEUTRAL_API_ERROR}), 502
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

        skin = _skin()
        user_message, history, error = _read_chat_request(skin)
        if error:
            return error

        group = Group.query.filter_by(name=slug).first()
        if group and group.tokens_remaining <= 0:
            return jsonify({'error': 'Token budget exhausted. Contact your instructor.'}), 403

        # Read these outside generate(). The reason is NOT that the request
        # context is gone inside it — that was the stated reason here for
        # months and it is false. `stream_with_context` below keeps the
        # context alive for the generator's lifetime; that is what it is for,
        # and the generator already proves it by running Group.query and
        # db.session.commit().
        #
        # The real constraint: returning Response() commits the status line,
        # so nothing inside generate() can emit a 403 or 409 — a rejection
        # would arrive as an SSE error event that the client has to notice —
        # and session mutations inside it never reach a Set-Cookie header.
        # So anything that decides *whether to answer at all* belongs above
        # this line, next to the budget check.
        skin_context = load_skin_context(slug)
        skin_persona = load_skin_persona(slug)
        skin_notes = load_skin_notes(slug)
        model = skin['model']
        api_options = _api_options(skin)
        neutral = skin.get('chrome') == 'neutral'

        def generate():
            full_text = ''
            total_tokens = 0
            try:
                for chunk, tokens in stream_claude_response(
                    skin_context, history, user_message,
                    model=model, persona=skin_persona, notes=skin_notes,
                    **api_options,
                ):
                    if chunk:
                        full_text += chunk
                        yield f'data: {json.dumps({"chunk": chunk})}\n\n'
                    elif tokens:
                        total_tokens = tokens
            except RuntimeError as e:
                if neutral:
                    current_app.logger.error(
                        'Claude API error for %s (%s)', slug, type((e.__cause__ or e)).__name__)
                    message = NEUTRAL_API_ERROR
                else:
                    message = str(e)
                yield f'data: {json.dumps({"error": message})}\n\n'
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
