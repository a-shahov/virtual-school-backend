from flask import Flask

from virtual_school_backend.auth import bp as auth_bp
from virtual_school_backend.main import bp as main_bp
from virtual_school_backend.user import bp as user_bp


def create_app():
    app = Flask(__name__)
    return app