"""User's authentication model"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """
    Create Django custom user(define their own Manager class)
    By inherit from BaseUserManager, get a lot of the same code that Django used to create the User
    """

    def create_user(self, username, email, password=None):
        """Creates and returns a user with an email, password, and username."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """Creates and returns superadmin user"""
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User's model"""
    username = models.CharField(db_index=True, max_length=127, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # The timestamp of the object's creation, haven't been change after .save()
    created_at = models.DateTimeField(auto_now_add=True)
    # The timestamp indicating the time the object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # The USERNAME_FIELD - field will use to log in. In this case, we want to use mail.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Define manager
    objects = UserManager()
