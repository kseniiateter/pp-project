from flask import Blueprint

api_blueprint = Blueprint('api_blueprint', __name__)


@api_blueprint.route('/hello-world-9')
def index():
    return "Hello World 9!"