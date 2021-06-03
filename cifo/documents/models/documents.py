"""Documents model."""

# Django
from django.db import models

# Utilities
from cifo.utils.models import CIFOModel

class Documents(CIFOModel):
  """Documents model."""

  user = models.ForeignKey('users.User', on_delete=models.CASCADE)

  # Documents
  title = models.CharField(max_length=100, blank=False, null=False, unique=True)
  file = models.FileField(upload_to='users/documents/', blank=False, null=False)
  url = models.CharField(max_length=255, blank=False, null=False)

  is_verified = models.BooleanField(default=False)

  def __str__(self):
    return str(f"{self.user}: {self.title}")