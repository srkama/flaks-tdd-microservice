from sqlalchemy import exc
from project.api.models import User
from project import db
from project import helpers

def create_user(post_json):
    invalid_response = {
        'status': 'error',
        'message': 'invalid payload'
    }
    if 'username' not in post_json or 'email' not in post_json or 'password' not in post_json:
        return invalid_response, 400, None

    try:
        username = post_json['username'].lower()
        email = post_json['email']
        password = post_json['password']

        if not helpers.validate_email(email):
            return invalid_response, 400, None

        if not helpers.validate_password(password):
            return invalid_response, 400, None

        user = User.query.filter_by(email=email).first()

        if user:
            invalid_response['message'] = 'Email id already exists'
            return invalid_response, 400, None
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': f'{post_json["email"]} was added!'
        }
        return response_object, 201, user
    except exc.IntegrityError:
        db.session.rollback()
        return invalid_response, 400, None
