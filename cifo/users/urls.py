"""Users URLs."""

# Django
from django.urls import path, include

# DRF Simple JWT
from rest_framework.routers import DefaultRouter

# DRF Simple JWT
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)

# Views
from cifo.users.views import UserLoginAPIView
from .views import users as user_views
from .views import documents as documents_views

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')
router.register(
  r'users/(?P<identification>[-0-9_-]+)/documents',
  documents_views.UserDocumentsViewSet,
  basename='user_documents'
)

urlpatterns = [
  path('users/login/', UserLoginAPIView.as_view(), name='login'),
  path('users/refresh/',  user_views.UserTokenRefreshView.as_view(), name='token_refresh'),
  path('', include(router.urls)),
]