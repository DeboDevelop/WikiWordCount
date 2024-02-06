from flask import Blueprint

api_bp = Blueprint('api', __name__)

@api_bp.route('/hello', methods=['GET'])
def hello_world():
    return {'message': "Hello World!!!"}
