from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from project.api.models import User
from project.api.user_helpers import create_user
from project import db
from project import helpers


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    response, status_code, user = create_user(request.get_json())
    return jsonify(response), status_code

@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        response_object = {
            'status': 'success',
            'data': {
                'username': user.username,
                'email': user.email,
                'active': user.active
            }
        }
        return jsonify(response_object), 200
    else:
        response_object = {
            'status': 'error',
            'message': 'user not found'
        }
        return jsonify(response_object), 404



@users_blueprint.route('/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    response_object = {
        'status': 'success',
        'data': [user.to_json() for user in users]
    }
    return jsonify(response_object), 200
