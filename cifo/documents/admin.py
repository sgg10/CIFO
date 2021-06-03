"""Documents admin."""

# Django
from django.contrib import admin

# Models
from cifo.documents.models import Documents

@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
  """License admin."""
  list_display = (
    'user',
    'title',
    'url',
    'is_verified'
  )
  search_fields = (
    'title',
    'user__username',
    'user__name'
  )
