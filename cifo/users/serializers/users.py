"""Users Serializers."""

# Django
from django.contrib.auth import authenticate, password_validation
from django.conf import settings

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.state import token_backend

# Models
from cifo.users.models import User

# Tasks
from cifo.taskapp.tasks import send_confirmation_email

# Utilities
import jwt
import requests
from datetime import timedelta

# Serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

BASE_URL = "https://govcarpetaapp.mybluemix.net/apis"

class UserModelSerializer(serializers.ModelSerializer):
  """User model serializer."""

  class Meta:
    """Meta class."""
    model = User
    fields = (
      'identification',
      'name',
      'email',
      'address',
      'operatorName'
    )

class UserLoginSerializer(TokenObtainPairSerializer):
  """User login serializer.
    Handle the login request data.
  """

  def validate(self, attrs):
    """Check credentials and get token."""
    user = authenticate(username=attrs['email'], password=attrs['password'])
    if not user:
      raise serializers.ValidationError('Invalid credentials')
    if not user.is_verified:
      raise serializers.ValidationError('Account is not active yet.')
    refresh = self.get_token(user)
    data = {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserModelSerializer(user).data
    }
    return data

class UserSignUpSerializer(serializers.Serializer):
  """User Sign up serializer.
    Handle sign up data validation and user creation.
  """

  email = serializers.EmailField(
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  identification = serializers.IntegerField(
    validators=[UniqueValidator(queryset=User.objects.all())]
  )

  # Password
  password = serializers.CharField(min_length=8)
  password_confirmation = serializers.CharField(min_length=8)

  # Name
  name = serializers.CharField(min_length=2, max_length=50)

  address = serializers.CharField(max_length=100)

  def validate(self, data):
    """Verify passwords match and the same user doesn't exist in another operator."""
    if len(str(data["identification"])) < 10:
      raise serializers.ValidationError("Identification cannot be less than 10 digits")

    response = requests.get(f'{BASE_URL}/validateCitizen/{data["identification"]}')
    if response.status_code != 204:
      raise serializers.ValidationError(response.text)

    passwd = data['password']
    passwd_conf = data['password_confirmation']
    if passwd != passwd_conf:
      raise serializers.ValidationError('Passwords don\'t match.')
    password_validation.validate_password(passwd)
    return data

  def create(self, data):
    """Handle user and profile creation."""
    data.pop('password_confirmation')
    user = User.objects.create_user(**data, operatorId = 20, operatorName="CIFO", is_verified=False, username=data["email"])
    send_confirmation_email.delay(user_pk=user.pk)
    return user

class AccountVerificationSerializer(serializers.Serializer):
  """Account verification serializer."""

  token = serializers.CharField()

  def validate_token(self, data):
    """Verify token is valid."""
    try:
      payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise serializers.ValidationError('Verification link has expired.')
    except jwt.PyJWTError:
      raise serializers.ValidationError('Invalid token')

    if payload['type'] != 'email_confirmation':
      raise serializers.ValidationError('Invalid token')

    self.context['payload'] = payload
    return data

  def save(self):
    """Update user's verified status"""
    payload = self.context['payload']
    user = User.objects.get(email=payload['user'])

    if not user.is_verified:
      url = f"{BASE_URL}/registerCitizen"

      response = requests.post(url, json={
        "id": user.identification,
        "name": user.name,
        "address": user.address,
        "email": user.email,
        "operatorId": 20,
        "operatorName": "CIFO"
      })
      if response.status_code != 201:
        raise serializers.ValidationError(response.text)

      user.is_verified = True
    user.save()

class UserTokenRefreshSerializer(TokenRefreshSerializer):
  """User token refresh serializer."""

  def validate(self, attrs):
    data = super(UserTokenRefreshSerializer, self).validate(attrs)
    decoded_payload = token_backend.decode(data['access'], verify=True)
    user_id = decoded_payload['user_id']
    data['user'] = UserModelSerializer(User.objects.get(id=user_id)).data
    return data