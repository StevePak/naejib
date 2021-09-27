from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:register')
TOKEN_URL = reverse('user:login')
USER_URL = reverse('user:index')


def create_user(**args):
    return get_user_model().objects.create_user(**args)


class PublicUserApiTests(TestCase):
    """Tests the public user api routes"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass',
            'first_name': 'Michael',
            'last_name': 'Scott'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_exists_fails(self):
        """Tests creating a user that exists fails"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass',
            'first_name': 'Michael',
            'last_name': 'Scott'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test password must be more than 5 characters"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'first_name': 'Michael',
            'last_name': 'Scott'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """test token is created for the user"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass',
            'first_name': 'Michael',
            'last_name': 'Scott'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_creds(self):
        """test token is not created for invalid creds"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass',
            'first_name': 'Michael',
            'last_name': 'Scott'
        }
        create_user(**payload)
        payload['password'] = 'passtest'

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """test token is not created for invalid creds"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass',
            'first_name': 'Michael',
            'last_name': 'Scott'
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """test token is not created for invalid creds"""
        payload = {
            'email': 'test@example.com',
            'password': '',
            'first_name': 'Michael',
            'last_name': 'Scott'
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """test that auth is required to get user details"""
        res = self.client.get(USER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test user api requests that require auth"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass',
            first_name='Michael',
            last_name='Scott'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_user_profile(self):
        """test retrieve user profile for logged in user"""
        res = self.client.get(USER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
        })

    def test_post_user_not_allowed(self):
        """test post not allowed on user root"""
        res = self.client.post(USER_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_full_update_user(self):
        """Test updating user profile"""
        payload = {
            'first_name': 'Dwight',
            'last_name': 'Schrute',
            'email': 'schrute@dundermifflin.com',
            'password': 'beets123'
        }

        res = self.client.patch(USER_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_partial_update_user(self):
        """Test updating user profile"""
        payload = {
            'first_name': 'Dwight',
            'last_name': 'Schrute'
        }

        res = self.client.patch(USER_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
