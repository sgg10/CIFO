"""Documents URLs."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import documents as documents_views
router = DefaultRouter()
router.register(r'documents', documents_views.DocumentsViewSet, basename='documents')

urlpatterns = [
  path('', include(router.urls))
]
