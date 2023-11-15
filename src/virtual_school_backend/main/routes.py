from flask import jsonify

from virtual_school_backend import db
from virtual_school_backend.models import Main, News
from virtual_school_backend.main import bp


@bp.route('/info', methods=['GET'])
def get_info():
    main = Main.query.first()
    return jsonify(title=main.description)

@bp.route('/info', methods=['PUT'])
def create_info():
    return 'hello world'

@bp.route('/news', methods=['GET'])
def get_news():
    return 'hello world'

@bp.route('/news', methods=['POST'])
def create_news():
    return 'hello world'

@bp.route('/news', methods=['PATCH'])
def update_news():
    return 'hello world'

@bp.route('/news', methods=['DELETE'])
def delete_news():
    return 'hello world'

@bp.route('/courses', methods=['GET'])
def get_courses():
    return 'hello world'

@bp.route('/courses', methods=['POST'])
def create_courses():
    return 'hello world'

@bp.route('/courses', methods=['PATCH'])
def update_courses():
    return 'hello world'

@bp.route('/courses', methods=['DELETE'])
def delete_courses():
    return 'hello world'
