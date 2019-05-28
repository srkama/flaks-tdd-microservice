from project import db, bcrypt
import jwt
import datetime
from flask import current_app

#User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password =  db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode()

    def to_json(self):
        return {
            'username':self.username,
            'email':self.email,
            'id':self.id,
            'active':self.active
        }

    def encode_auth_token(self):
        try:
            payload =  {
                'sub':self.id,
                'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=current_app.config['TOKEN_EXPIRATION_SECONDS']),
                'iat':datetime.datetime.utcnow()
            }
            token =  jwt.encode(payload,current_app.config.get('SECRET_KEY'),algorithm='HS256')
            return token
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
