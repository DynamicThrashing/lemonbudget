from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Our custom user manager
class CustomUserManager(BaseUserManager):
    """
    Model manager for our custom user model,
    which uses email instead of username for the unique identifier
    """

    def create_user(self, email, password, **extra_fields):
        """
        create and save a custom user with the given email and password
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        if not email:
            raise ValueError(_("Please enter an email"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with the given email and password
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


# Create your models here.
class CustomUser(AbstractUser):
    """
    Our Custom User Model that uses email instead of the username.
    """

    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
