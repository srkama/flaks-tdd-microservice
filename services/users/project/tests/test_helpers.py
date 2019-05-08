import unittest
from parameterized import parameterized
from project.helpers import validate_email, validate_password
from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):

    @parameterized.expand([
        ('empty_value',''),
        ('kamal','kamal'),
        ('kamal@gc','kamal@gc'),
        ('l@gc','l@gc'),
        ('kamal@gc..com','kamal@gc..com'),
        ('kamal@@gc.','kamal@@gc.'),
        ('kamal@gc.','kamal@gc.'),
        ('kamal&s@gmail.com','kamal&s@gmail.com'),
    ])
    def test_validate_invalid_email(self,name,input):
        self.assertFalse(validate_email(input))

    @parameterized.expand([
        ('kamal@gc.com','kamal@gc.com'),
        ('kamal@gmail.com','kamal@gmail.com'),
        ('kamal_s@gmail.com','kamal_s@gmail.com'),
        ('kamal.s@gmail.com','kamal.s@gmail.com'),
    ])
    def test_validate_email(self,name,input):
        self.assertTrue(validate_email(input))

    @parameterized.expand([
        ('1aa1aa','1aa1aa'),
        ('aaaaa1','aaaaa1'),
        ('&aaaa1','&aaaa1'),
    ])
    def test_validate_password(self,name, input):
        self.assertTrue(validate_password(input))

    @parameterized.expand([
        ('1aa1a','1aa1a'),
        ('111111','111111'),
        ('aaaaaa','aaaaaa'),
        ('&aa1','&aa1'),
    ])
    def test_validate_password(self,name, input):
        self.assertFalse(validate_password(input))

if __name__ == "__main__":
    unittest.main()
