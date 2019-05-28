import os
import unittest
from flask import current_app
from flask_testing import TestCase
from project import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_development_config(self):
        self.assertTrue(app.config['SECRET_KEY']==os.environ.get('DEV_SECRET_KEY'))
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['TOKEN_EXPIRATION_SECONDS']==900)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_DEV_URL'))

class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_production_config(self):
        self.assertTrue(app.config['SECRET_KEY']==os.environ.get('PROD_SECRET_KEY'))
        self.assertFalse(app.config['TESTING'])
        self.assertTrue(app.config['TOKEN_EXPIRATION_SECONDS']==1800)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_URL'))


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_testing_config(self):
        self.assertTrue(app.config['SECRET_KEY']==os.environ.get('DEV_SECRET_KEY'))
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(app.config['TOKEN_EXPIRATION_SECONDS']==900)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_TEST_URL'))


if __name__ == "__main__":
    unittest.main()
