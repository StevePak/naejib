from django.utils import timezone
from core import models
from django.test import TestCase
from django.contrib.auth import get_user_model

from unittest.mock import patch


class UserModelTests(TestCase):

    def setUp(self):
        self.defaultUser = {
            "email": "test@example.com",
            "first_name": "Michael",
            "last_name": "Scott",
            "password": "testpass123"
        }

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


class LinkModelTests(TestCase):

    def setUp(self):
        self.defaultUser = {
            "email": "test@example.com",
            "first_name": "Michael",
            "last_name": "Scott",
            "password": "testpass123"
        }

    def test_create_new_link_is_successful(self):
        """Tests creating a new link with full details is successful"""
        default = self.defaultUser.copy()
        user = get_user_model().objects.create_user(**default)

        link = models.Link.objects.create(
            url='www.test.com', description='test url', order=0, user_id=user.id)

        self.assertEqual(link.url, 'www.test.com')
        self.assertEqual(link.description, 'test url')
        self.assertEqual(link.order, 0)
        self.assertEqual(link.user, user)


class NoteModelTests(TestCase):

    def setUp(self):
        self.defaultUser = {
            "email": "test@example.com",
            "first_name": "Michael",
            "last_name": "Scott",
            "password": "testpass123"
        }

    def test_create_new_note_is_successful(self):
        """Tests creating a new link with full details is successful"""
        default = self.defaultUser.copy()
        user = get_user_model().objects.create_user(**default)
        datetime = timezone.now()

        title = 'Note'
        content = "this is my new note"

        with patch('django.utils.timezone.now') as now:
            now.return_value = datetime
            note = models.Note.objects.create(
                title=title, content=content, user_id=user.id)

            self.assertEqual(note.title, title)
            self.assertEqual(note.content, content)
            self.assertEqual(note.created_date, datetime)
            self.assertEqual(note.last_updated_date, datetime)
            self.assertEqual(note.user, user)
            self.assertFalse(note.hasBeenEdited())

    def test_editing_note(self):
        """Tests editing a note"""
        default = self.defaultUser.copy()
        user = get_user_model().objects.create_user(**default)

        title = 'Note'
        content = "this is my new note"

        note = models.Note.objects.create(
            title=title, content=content, user_id=user.id)

        self.assertEqual(note.created_date, note.last_updated_date)
        self.assertFalse(note.hasBeenEdited())

        new_content = "this is my note edited"
        note.content = new_content
        note.save()

        self.assertEqual(note.content, new_content)
        self.assertNotEqual(note.created_date, note.last_updated_date)
        self.assertTrue(note.hasBeenEdited())
