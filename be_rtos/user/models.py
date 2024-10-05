from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from uuid import uuid4
from firebase_admin import messaging

class UserManager(BaseUserManager):
    """User manager for creating users and superusers"""

    def create_user(self, email: str, password: str, **extra_fields: dict) -> 'User':
        """
        Create and saves new user
        :param email: user email
        :param passsowrd: user password
        :param extra_fields
        """
        if not email:
            raise ValueError('Email must not be empty')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email: str, password: str, **extra_fields: dict) -> 'User':
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(unique=True, default=uuid4, editable=False, primary_key=True)
    email = models.EmailField(
        max_length=255,
        unique=True,
        error_messages={'unique': 'email_already_used'},
        verbose_name=("Email"),
    )
    first_name = models.CharField(
        max_length=255,
        blank=False,
    )
    last_name = models.CharField(
        max_length=255,
        blank=False
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Is Staff?',
        help_text="Use this iption for create staff"
    )
    fcm_token = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=None,
    )
    date_of_birth = models.DateField(
        blank=False,
    )
    gender = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    
    def __str__(self) -> str:
        return self.get_full_name() + '- ' + str(self.pk)