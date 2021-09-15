from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):

    def setUp(self):
        self.defaultUser = {
            "email": "test@example.com",
            "first_name": "Michael",
            "last_name": "Scott",
            "password": "testpass123"
        }
        return super().setUp()

    def test_create_new_user_is_successful(self):
        """Tests creating a new user with full details is successful"""

        user = get_user_model().objects.create_user(**self.defaultUser)

        self.assertEqual(user.email, self.defaultUser['email'])
        self.assertTrue(user.check_password(self.defaultUser['password']))

    def test_new_user_email_lower(self):
        email = "test@EXAMPLE.COM"
        defaults = self.defaultUser.copy()
        defaults['email'] = email

        user = get_user_model().objects.create_user(**defaults)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test created with invalid email raises error"""
        email = "test"
        defaults = self.defaultUser.copy()
        defaults['email'] = email

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(**defaults)
