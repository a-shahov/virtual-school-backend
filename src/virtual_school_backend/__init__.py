from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from virtual_school_backend.config import Config

db = SQLAlchemy()
migrate = Migrate()

from virtual_school_backend.auth import bp as auth_bp
from virtual_school_backend.main import bp as main_bp
from virtual_school_backend.user import bp as user_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)

    return app