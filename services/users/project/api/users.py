from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from project.api.models import User
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
    post_json = request.get_json()
    invalid_response = {
        'status': 'error',
        'message': 'invalid payload'
    }
    if 'username' not in post_json or 'email' not in post_json:
        return jsonify(invalid_response), 400

    try:
        username = post_json['username']
        email = post_json['email']

        if not helpers.validate_email(email):
            return jsonify(invalid_response), 400
        user = User.query.filter_by(email=email).first()

        if user:
            invalid_response['message'] = 'Email id already exists'
            return jsonify(invalid_response), 400
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': f'{post_json["email"]} was added!'
        }
        return jsonify(response_object), 201
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(invalid_response), 400


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
