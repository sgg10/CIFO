""" Documents views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (IsAuthenticated)

# Models
from cifo.documents.models import Documents

# Serializers
from cifo.documents.serializers import UploadDocumentsSerializer, VerifiedDocumentSerializer

class DocumentsViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
  """Documents view set."""

  serializer_class = UploadDocumentsSerializer

  def get_permissions(self):
    permissions = [IsAuthenticated]
    return [permission() for permission in permissions]

  @action(detail=False, methods=['POST'])
  def upload(self, request):
    print(request.data)
    serializer = UploadDocumentsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(request.user)
    return Response({ 'message': f'File {request.data["title"]} was uploaded successfully' }, status=status.HTTP_200_OK)

  @action(detail=False, methods=['POST'])
  def authenticate(self, request):
    """Document authentication."""
    serializer = VerifiedDocumentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(request.user)
    data = { 'message': 'Congratulation, your document has been authenticated!' }
    return Response(data, status=status.HTTP_200_OK)

