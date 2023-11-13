from flask import Blueprint


bp = Blueprint('auth', __name__)

from virtual_school_backend.auth import routes