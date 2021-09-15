from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_new_user_is_successful(self):
        """Tests creating a new user with full details is successful"""
        email = "test@example.com"
        first_name = "Michael"
        last_name = "Scott"
        password = "testpass123"

        user = get_user_model().objects.create_user(email=email, password=password,
                                                    first_name=first_name, last_name=last_name)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
