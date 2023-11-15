from flask import Blueprint


bp = Blueprint('main', __name__, url_prefix='/main')

from virtual_school_backend.main import routes