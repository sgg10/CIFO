"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Models
from cifo.users.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
  list_display = (
    'identification',
    'email',
    'name',
    'operatorId',
    'operatorName',
    'is_verified'
  )
  search_fields = ('email', 'name', 'identification', 'operatorName')
  list_filter = ('created', 'modified', 'is_verified')