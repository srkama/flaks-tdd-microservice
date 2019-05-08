
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
        user = User(username='kamal1',email='kamal.s@gc.com', password="gc!sfdklas")
        db.session.add(user)
        self.assertNotEqual(self.user.password, user.password)
