"""Documents serializer."""

# Django REST Framework
from rest_framework import serializers

# models
from cifo.documents.models import Documents

# Base
from config.settings.base import firebase

# Utilities
import requests

BASE_URL = "https://govcarpetaapp.mybluemix.net/apis"

class DocumentsModelSerializer(serializers.ModelSerializer):
  """Documents model serializer."""

  class Meta:
    model = Documents
    fields = [
      'user',
      'title',
      'url',
      'is_verified'
    ]
    read_only_fields = (
      'user',
      'title',
      'url',
      'is_verified'
    )

class UploadDocumentsSerializer(serializers.Serializer):
  """Upload Documents serializer."""

  file = serializers.FileField()
  title = serializers.CharField()

  def validate(self, data):
    if "file" not in data.keys():
      raise serializers.ValidationError("Request body does not have 'file' field")
    if "title" not in data.keys():
      raise serializers.ValidationError("Request body does not have 'title' field")
    self.context["file"] = data["file"]
    self.context["title"] = data["title"]
    return data

  def save(self, user):
    storage = firebase.storage()
    cloudFileName= f"documents/{user.identification}/{self.context['title']}"
    storage.child(cloudFileName).put(self.context["file"])
    documentUrl = storage.child(cloudFileName).get_url(None)
    document = Documents(
      user=user,
      file=self.context["file"],
      title=self.context["title"],
      url=documentUrl
    )
    document.save()

class VerifiedDocumentSerializer(serializers.Serializer):
  """Verified DOcuments serializer."""
  title = serializers.CharField()
  url = serializers.CharField()

  def validate(self, data):
    self.context["title"] = data["title"]
    self.context["url"] = data["url"]
    self.context["configured_url"] = self.context["url"].replace(":", "%3A").replace("%2F", "%252").replace("/", "%2F").replace("?", "%3F").replace("=", "%3D")
    print(self.context["configured_url"])
    return data

  def save(self, user):
    try:
        self.context["document"] = Documents.objects.get(
          user=user,
          title=self.context["title"],
          url=self.context["url"]
        )
    except Documents.DoesNotExist:
      raise serializers.ValidationError("This file does not exist.")

    if not self.context["document"].is_verified:
      url = f"{BASE_URL}/authenticateDocument/{user.identification}/{self.context['configured_url']}/{self.context['title']}"
      response = requests.get(url)
      if response.status_code > 204:
        raise serializers.ValidationError(response.text)
      self.context["document"].is_verified = True
    self.context["document"].save()