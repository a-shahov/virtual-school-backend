from flask import Blueprint


bp = Blueprint('main', __name__)

from virtual_school_backend.main import routes