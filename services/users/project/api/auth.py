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
        response['token'] = user_obj.encode_auth_token()
    return jsonify(response), status_code

@auth_blueprint.route('/auth/login', methods=['POST'])
def auth_login():
    INVALID_PAYLOAD_MESSAGE = {
        'status':'error',
        'message': 'Invalid Payload'
    }
    post_json = request.get_json()

    if 'username' not in post_json or 'password' not in post_json:
        return jsonify(INVALID_PAYLOAD_MESSAGE), 400

    user = User.query.filter_by(username=post_json['username'].lower()).first()
    if user and bcrypt.check_password_hash(user.password, post_json['password']):
        response = {
            'message': 'successfully logged in!',
            'token': user.encode_auth_token(),
            'username': user.username
        }
        return jsonify(response), 200
    else:
        response = {
            'message':'Username or Password doesn\'t match our records',
                'status':'error'
        }
        return jsonify(response), 400

@auth_blueprint.route('/auth/logout', methods=['GET'])
def auth_logout():
    auth_header = request.headers.get('Authorization')
    INVALID_MESSAGE = {'status':'fail','message':'Token missing'}
    resp = ""
    try:
        token = auth_header.split(' ')
        resp = User.decode_auth_token(token[1])
        print(resp)
        if not isinstance(resp, str):
            return jsonify({'status':'success', 'message':'logged out'}), 200
    except Exception as e:
        resp=str(e)
        print(resp)
    return jsonify({'status':'fail', 'message': resp}), 401

@auth_blueprint.route('/auth/status', methods=['GET'])
def auth_status():
    auth_header = request.headers.get('Authorization')
    resp = ""
    try:
        token = auth_header.split(' ')[1]
        response = User.decode_auth_token(token)
        if(isinstance(response, User)):
            data = {
                'status':'success',
                'data': response.to_json()
            }
            status_code=200
        else:
            data = {
                'status': 'fail',
                'message': response
            }
            status_code=401
        return jsonify(data), status_code
    except Exception as e:
        resp = str(e)
    return jsonify({'status':'fail', 'message': resp}), 401
