from flask import Blueprint, render_template, redirect, url_for, session
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
    return render_template('login.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@main.route('/chat')
@group_login_required
def chat():
    return render_template('chat.html')


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
