import os
from flask import Flask
from dotenv import load_dotenv

from models import db

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-change-me')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'sqlite:///ta_system.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD', 'admin')

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=int(os.getenv('PORT', '5000')), debug=True)
