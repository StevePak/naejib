from django.utils import timezone
from django.conf import settings
from utils import validators
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email: str, password: str, first_name: str, last_name: str) -> "User":
        """creates a new user using provided details"""
        if not validators.isEmailValid(email):
            raise ValueError('User must have valid email address.')

        user = self.model(email=email.lower(), first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User Model"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Link(models.Model):
    url = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    order = models.IntegerField()

    def __str__(self):
        """string representation of link"""
        return """
        ${self.description}
        ${self.url}
        """


class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_date = models.DateTimeField()
    last_updated_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        now = timezone.now()
        self.created_date = self.created_date or now
        self.last_updated_date = now
        super().save(*args, **kwargs)

    def hasBeenEdited(self):
        return self.created_date != self.last_updated_date

    def __str__(self):
        """string representation of a Note"""
        return """
        ${self.title}
        ${self.content}
        """
