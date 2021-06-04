"""Users views."""

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Permissions
from rest_framework.permissions import (
  AllowAny,
  IsAuthenticated
)
from cifo.users.permissions import IsAccountOwner

# Serializer
from cifo.users.serializers.users import (
  UserLoginSerializer,
  UserModelSerializer,
  UserSignUpSerializer,
  AccountVerificationSerializer,
  UserTokenRefreshSerializer
)

# Models
from cifo.users.models import User

class UserLoginAPIView(TokenObtainPairView):
  """User login API view."""
  serializer_class = UserLoginSerializer

class UserTokenRefreshView(TokenRefreshView):
  """Custom user token refresh view."""
  serializer_class = UserTokenRefreshSerializer

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
  """User view set.
    Handle sign up, login and account verification
  """

  queryset = User.objects.filter(is_active=True)
  serializer_class = UserModelSerializer
  lookup_field = 'identification'

  def get_permissions(self):
    """Assing permissions based on action."""
    if self.action in ['signup', 'login', 'verify']:
      permissions = [AllowAny]
    elif self.action in ['retrieve', 'update', 'partial_update', 'profile']:
      permissions = [IsAuthenticated, IsAccountOwner]
    else:
      permissions = [IsAuthenticated]
    return [permission() for permission in permissions]

  @action(detail=False, methods=['POST'])
  def signup(self, request):
    """User sing up."""
    serializer = UserSignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    data = UserModelSerializer(user).data
    return Response(data, status=status.HTTP_201_CREATED)

  @action(detail=False, methods=['POST'])
  def verify(self, request):
    """User account verification."""
    serializer = AccountVerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    data = { 'message': 'Congratulation, now go to upload some files!' }
    return Response(data, status=status.HTTP_200_OK)