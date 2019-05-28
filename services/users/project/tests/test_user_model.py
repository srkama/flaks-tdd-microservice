
from project.api.models import User
from project import db
from base import BaseTestCase

from sqlalchemy.exc import IntegrityError


class TestUserModel(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user = User(username='kamal',email='kamal.s@gc.com', password="gc!sfdklas")
        db.session.add(self.user)
        db.session.commit()

    def test_add_user(self):
        self.assertTrue(self.user.id)
        self.assertEqual(self.user.username,'kamal')
        self.assertEqual(self.user.email,'kamal.s@gc.com')

    def test_user_to_json(self):
        self.assertTrue(isinstance(self.user.to_json(),dict))

    def test_not_allow_duplicate_username(self):
        user = User(username='kamal',email='kamal1.s@gc.com', password="gc!sfdklas")
        db.session.add(user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_not_allow_duplicate_email(self):
        user = User(username='kamal1',email='kamal.s@gc.com', password="gc!sfdklas")
        db.session.add(user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_two_passwords_are_not_same(self):
        user = User(username='kamal1',email='kamal.s1@gc.com', password="gc!sfdklas")
        db.session.add(user)
        db.session.commit()
        self.assertNotEqual(self.user.password, user.password)

    def test_encode_auth_token(self):
        user = User(username='kamal1',email='kamal.s1@gc.com', password="gc!sfdklas")
        db.session.add(user)
        db.session.commit()
        token = user.encode_auth_token()
        self.assertTrue(isinstance(token,bytes))

    def test_decode_auth_token(self):
        user = User(username='kamal1',email='kamal.s1@gc.com', password="gc!sfdklas")
        db.session.add(user)
        db.session.commit()
        token = user.encode_auth_token()
        user_id = User.decode_auth_token(token)
        self.assertTrue(user_id == user.id)
