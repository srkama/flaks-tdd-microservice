import json
import unittest
from parameterized import parameterized
from project.tests.base import BaseTestCase
from project.api.models import User
from project import db


class TestUserService(BaseTestCase):

    def test_ping_pong(self):
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])

    def test_add_users(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'kamal',
                    'email': 'kamal.s@gc.com'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('kamal.s@gc.com was added!', data['message'])
            self.assertIn('success', data['status'])

    @parameterized.expand([
        ("kamals@gc",{'username':'kamal','email':'kamals@gc'}),
        ("kamal&s@gc.com",{'username':'kamal','email':'kamal&s@gc.com'}),
    ])
    def test_add_user_with_invalid_email(self, name, input):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(input),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('invalid payload', data['message'])
            self.assertIn('error', data['status'])

    @parameterized.expand([
        ("empty payload",{}),
        ("username is missing",{'email':'kamal.s@gc.com'}),
        ("emailid is missing",{'username':'kamal'}),
    ])
    def test_add_user_with_invalid_payload(self, name, input):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(input),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('invalid payload', data['message'])
            self.assertIn('error', data['status'])

    def test_add_user_duplicate_users(self):
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'kamal',
                    'email': 'kamal.s@gc.com'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'kamal',
                    'email': 'kamal.s@gc.com'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Email id already exists', data['message'])
            self.assertIn('error', data['status'])

    def test_get_user(self):
        user = User(username='kamal',email='kamal.s@gc.com')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('kamal', data['data']['username'])
            self.assertIn('kamal.s@gc.com', data['data']['email'])
            self.assertTrue(data['data']['active'])

    def test_get_user_invalid_user(self):
        user = User(username='kamal',email='kamal.s@gc.com')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.get(f'/users/3')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 404)
            self.assertIn('user not found', data['message'])
            self.assertIn('error', data['status'])

    def test_get_users(self):
        users = [
            User(username='kamal1',email='kamal1.s@gc.com'),
            User(username='kamal',email='kamal.s@gc.com'),
        ]
        db.session.add_all(users)
        db.session.commit()
        with self.client:
            response = self.client.get(f'/users/')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['data'][0]['username'], 'kamal1')
            self.assertEqual(data['data'][0]['email'],'kamal1.s@gc.com')
            self.assertEqual(data['data'][1]['username'],'kamal')
            self.assertEqual(data['data'][1]['email'],'kamal.s@gc.com')



if __name__ == '__main__':
    unittest.main()
