import time

from django.db import models
from django.contrib import auth
import uuid


class User(models.Model):
    """пользователь"""
    email = models.EmailField(primary_key=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    """маркер"""
    email = models.EmailField()
    uid = models.CharField(max_length=40, default=uuid.uuid4)
