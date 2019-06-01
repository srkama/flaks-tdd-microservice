import os

class BaseConfig:
    TESTING = False
    SECRET_KEY = "my_key"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    TOKEN_EXPIRATION_SECONDS = 1800  # new

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_DEV_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TOKEN_EXPIRATION_SECONDS = 900  # new


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TOKEN_EXPIRATION_SECONDS = 5  # new


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TOKEN_EXPIRATION_SECONDS = 1800  # new
