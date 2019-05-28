import json
import unittest
from parameterized import parameterized
from project.tests.base import BaseTestCase
from project.api.models import User
from project import db


class TestAuthService(BaseTestCase):

    def test_auth_registration(self):
        with self.client:
            response = self.client.post(
                '/auth/registration',
                data=json.dumps({
                    'username': 'kamal',
                    'email': 'kamal.s@gc.com',
                    'password': 'sdfkhasdf9au'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue('token' in data)
            self.assertEqual('kamal.s@gc.com', data['email'])
            self.assertEqual('kamal', data['username'])

    @parameterized.expand([
        ("empty payload",{}),
        ("username is missing",{'email':'kamal.s@gc.com'}),
        ("emailid is missing",{'username':'kamal'}),
        ("password is missing", {'username':'kamal', 'email':'kamal.s@gc.com'})
    ])
    def test_auth_registration_invalid_playload(self, name, input):
         with self.client:
            response = self.client.post(
                '/auth/registration',
                data=json.dumps(input),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['message'],'invalid payload')

    def test_auth_login(self):
        payload = {
            'username': 'kamals',
            'password': 'sldfjakwr23'
        }
        user = User(username='kamals', password='sldfjakwr23', email='kamal.s@gc.com')
        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(payload),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('token' in data)
            self.assertEqual(data['username'],'kamals')
            self.assertEqual(data['message'],'successfully logged in!')



if __name__ == '__main__':
    unittest.main()
