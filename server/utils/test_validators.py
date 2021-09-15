from django.test import TestCase
from . import validators


class EmailValidatorTests(TestCase):

    def test_valid_email(self):
        """Tests valid email"""
        email = "test@example.com"

        self.assertTrue(validators.isEmailValid(email))

    def test_email_no_at(self):
        """Tests email without @ sign"""
        email = "testexample.com"
        self.assertFalse(validators.isEmailValid(email))

    def test_email_no_dot(self):
        """Tests email without dot"""
        email = "test@examplecom"
        self.assertFalse(validators.isEmailValid(email))

    def test_email_dot_not_in_domain(self):
        """Tests email without dot in domain"""
        email = "test.email@examplecom"
        self.assertFalse(validators.isEmailValid(email))
