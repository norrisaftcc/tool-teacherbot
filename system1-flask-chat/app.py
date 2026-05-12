import os
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from models import db

load_dotenv()

login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__)

    # Config
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret')
    database_url = os.getenv('DATABASE_URL', 'sqlite:///ta_system.db')
    # Render gives postgres:// but SQLAlchemy 2.x requires postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD', 'admin')

    if test_config:
        app.config.update(test_config)

    # Extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # user_loader required by flask_login even though auth is session-based
    @login_manager.user_loader
    def load_user(user_id):
        return None

    # Blueprint (imported here to avoid circular imports)
    from routes import main
    app.register_blueprint(main)

    # Create tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
