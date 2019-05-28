from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from project.api.models import User
from project.api.user_helpers import create_user
from project import db, bcrypt
from project import helpers


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/auth/registration', methods=['POST'])
def auth_register():
    response, status_code, user_obj = create_user(request.get_json())
    if status_code == 201:
        response = user_obj.to_json()
        response['token'] = user_obj.encode_auth_token().decode()
    return jsonify(response), status_code

@auth_blueprint.route('/auth/login', methods=['POST'])
def auth_login():
    post_json = request.get_json()
    user = User.query.filter_by(username=post_json['username']).first()
    if user and bcrypt.check_password_hash(user.password, post_json['password']):
        response = {
            'message': 'successfully logged in!',
            'token': user.encode_auth_token().decode(),
            'username': user.username
        }
        return jsonify(response), 200
