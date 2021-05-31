"""User model"""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utilities
from cifo.utils.models import CIFOModel
import uuid

class User(CIFOModel, AbstractUser):
  """User model.
    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
  """
  identification = models.BigIntegerField(blank=False, null=False)

  name = models.CharField(max_length=50, blank=False, null=False)

  address = models.CharField(max_length=100, blank=False)

  operatorId = models.IntegerField(blank=False, null=False, default=20)
  operatorName = models.CharField(max_length=60, blank=False, null=False, default="CIFO")

  email = models.EmailField(
    'email address',
    unique=True,
    error_messages={
      'unique': 'A user with this email address already exists'
    }
  )

  is_verified=models.BooleanField(
    'verified',
    default=False,
    help_text='Set true when the user have verified its email address.'
  )

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['identification', 'name', 'address', 'username']

  def __str__(self):
    """Return name."""
    return self.name

  def get_short_name(self):
    """Return name."""
    return self.name