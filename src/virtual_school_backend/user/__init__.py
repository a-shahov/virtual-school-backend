from flask import Blueprint


bp = Blueprint('user', __name__)

from virtual_school_backend.user import routes