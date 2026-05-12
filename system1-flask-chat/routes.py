from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from functools import wraps

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


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
