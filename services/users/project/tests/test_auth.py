import json
import unittest
from parameterized import parameterized
from project.tests.base import BaseTestCase
from project.api.models import User
from project import db


class TestAuthService(BaseTestCase):

    @parameterized.expand([
        ("payload",{
                    'username': 'kamal',
                    'email': 'kamal.s@gc.com',
                    'password': 'sdfkhasdf9au'
                }),
        ("username with all uppercase",{
                    'username': 'KAMAL',
                    'email': 'kamal.s@gc.com',
                    'password': 'sdfkhasdf9au'
                }),
        ("username with radonw uppercase",{
                    'username': 'kAmAl',
                    'email': 'kamal.s@gc.com',
                    'password': 'sdfkhasdf9au'
                }),
    ])
    def test_auth_registration(self, name, payload):
        with self.client:
            response = self.client.post(
                '/auth/registration',
                data=json.dumps(payload),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue('token' in data)
            self.assertEqual('kamal.s@gc.com', data['email'])
            self.assertEqual(payload['username'].lower(), data['username'])

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

    @parameterized.expand([
        ('correct payload', {
            'username': 'kamals',
            'password': 'sldfjakwr23'
        }),
        ('payload with uppercase username', {
            'username': 'KAMALS',
            'password': 'sldfjakwr23'
        }),
    ])
    def test_auth_login(self, name, payload):
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

    @parameterized.expand([
        ("empty payload",{}),
        ("username is missing",{'password':'kamal.s@gc.com'}),
        ("password is missing",{'username':'kamal'}),
        ("username is missing",{'email':'kamal', 'password':'324shskdf'}),
        ("password spelling is wrong",{'username':'kamal', 'passwrd':'324shskdf'}),
        ("username spelling is wrong",{'usname':'kamal', 'password':'324shskdf'}),
    ])
    def test_auth_login_invalid_payload(self, name, payload):
      
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(payload),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['message'], 'Invalid Payload')
            self.assertEqual(data['status'], 'error')

    @parameterized.expand([
        ("username is wrong",{'username':'kamal.s@gc.com', 'password':'sldfjakwr23'}),
        ("password is wrong",{'username':'kamals', 'password':'sldkwr23'}),
    ])
    def test_auth_login_invalid_data(self, name, payload):
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
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data['message'], 'Username or Password doesn\'t match our records')
            self.assertEqual(data['status'], 'error')

    def test_auth_logout(self):
        user = User(username='kamals', password='sldfjakwr23', email='kamal.s@gc.com')
        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username':'kamals',
                    'password':'sldfjakwr23'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            token = data['token']
            
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'logged out')
            self.assertEqual(data['status'], 'success')
    
    def test_auth_logout_invalid(self):
        user = User(username='kamals', password='sldfjakwr23', email='kamal.s@gc.com')
        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username':'kamals',
                    'password':'sldfjakwr23'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            token = data['token']

            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer '}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['message'], 'Invalid token. Please log in again.')
            self.assertEqual(data['status'], 'fail')

    def test_auth_status(self):
        user = User(username='kamals', password='sldfjakwr23', email='kamal.s@gc.com')
        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username':'kamals',
                    'password':'sldfjakwr23'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            token = data['token']

            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['data']['email'],user.email)
            self.assertEqual(data['status'], 'success')

    def test_auth_status_invalid_token(self):
        user = User(username='kamals', password='sldfjakwr23', email='kamal.s@gc.com')
        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer sdfs'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['message'],'Invalid token. Please log in again.')
            self.assertEqual(data['status'], 'fail')    
    

if __name__ == '__main__':
    unittest.main()
