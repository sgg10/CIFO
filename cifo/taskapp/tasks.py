"""Celery tasks."""

# Django
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# Celery
from celery.decorators import task, periodic_task
from celery.task.schedules import crontab

# Models
from cifo.users.models import User

# Utilities
import jwt
from datetime import timedelta

def gen_verification_token(user):
  """Create JWT token that the user can use to verify its account."""
  exp_date = timezone.now() + timedelta(days=3)
  payload = {
    'user': user.username,
    'exp': int(exp_date.timestamp()),
    'type': 'email_confirmation'
  }
  token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
  return token

@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
  """Send account verification link to given user."""
  user = User.objects.get(pk=user_pk)
  verification_token = gen_verification_token(user)

  subject = f'Welcome @{user.username}! Verify your account to start using Citizen Folder'
  from_email = 'Citizen Folder <noreply@cifo.com'
  content = render_to_string(
    'emails/users/account_verification.html',
    { 'token': verification_token, 'user': user }
  )
  msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
  msg.attach_alternative(content, 'text/html')
  msg.send()