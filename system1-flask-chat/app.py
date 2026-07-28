import os
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from models import db

load_dotenv()

login_manager = LoginManager()

REQUIRED_SECRETS = ('SECRET_KEY', 'ADMIN_PASSWORD')

# The env var each config key comes from, for an error message an operator
# can act on without reading this file.
_SECRET_SOURCE = {'SECRET_KEY': 'FLASK_SECRET_KEY', 'ADMIN_PASSWORD': 'ADMIN_PASSWORD'}


def _require_secrets(app) -> None:
    """Refuse to build an app that is missing a secret.

    Checked *after* test_config is merged, so tests supply their own and
    never touch the environment. Local development gets these from a .env
    file — see .env.example, which lists both.
    """
    missing = [key for key in REQUIRED_SECRETS if not app.config.get(key)]
    if missing:
        names = ', '.join(_SECRET_SOURCE[key] for key in missing)
        raise RuntimeError(
            f'Refusing to start: {names} not set. Set them in the Render '
            f'dashboard (both are sync:false in render.yaml, so the Blueprint '
            f'does not provide them) or in a local .env — see .env.example. '
            f'Running without them would sign session cookies with a value '
            f'published in this repo.'
        )


def create_app(test_config=None):
    app = Flask(__name__)

    # Config
    #
    # SECRET_KEY and ADMIN_PASSWORD have no fallback outside tests, and that
    # is deliberate. Both are `sync: false` in render.yaml — Render does not
    # set them from the Blueprint, an operator does, by hand, once. The old
    # defaults ('dev-secret' and 'admin') meant a service that came up
    # without them looked completely healthy while signing session cookies
    # with a value published in this repo. Anyone could forge
    # session['skin'] and walk past the cohort passcode, and nothing
    # anywhere would say so.
    #
    # A service that refuses to boot is a worse outage and a much better
    # failure: it is loud, it is immediate, and DEPLOY.md tells the operator
    # exactly which variable to set.
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    database_url = os.getenv('DATABASE_URL', 'sqlite:///ta_system.db')
    # Normalize to postgresql+psycopg:// for psycopg3 dialect (Python 3.12+ compatible)
    if database_url.startswith('postgres://'):
        database_url = 'postgresql+psycopg://' + database_url[len('postgres://'):]
    elif database_url.startswith('postgresql://'):
        database_url = 'postgresql+psycopg://' + database_url[len('postgresql://'):]
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD')

    if test_config:
        app.config.update(test_config)

    _require_secrets(app)

    # Extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.index'

    # user_loader required by flask_login even though auth is session-based
    @login_manager.user_loader
    def load_user(user_id):
        return None

    # Blueprints (imported here to avoid circular imports).
    # `main` owns the root picker + logout; each skin gets its own blueprint
    # registered at /<slug> so URL is the source of truth for cohort + model.
    from routes import main, skin_blueprint
    from auth import SKINS
    app.register_blueprint(main)
    for slug in SKINS:
        app.register_blueprint(skin_blueprint(slug), url_prefix=f'/{slug}')

    # Create tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
