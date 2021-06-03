"""Documents permissions classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cifo.users.models import User
from cifo.documents.models import Documents

class IsDocumentOwner(BasePermission):
  """Allow access only to document owner."""

  def haspermission(self, request, view):
    """Check if user owns the document."""
    try:
      document = Documents.objects.get(
        user=request.user
      )
    except Documents.DoesNotExist:
      return False
    return True