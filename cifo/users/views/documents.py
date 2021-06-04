"""Documents Licenses views."""

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated
from cifo.users.permissions import IsAccountOwner

# Serializers
from cifo.documents.serializers import DocumentsModelSerializer

# Models
from cifo.users.models import User
from cifo.documents.models import Documents

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class UserDocumentsViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
  """User documents view set."""

  serializer_class = DocumentsModelSerializer
  queryset = Documents.objects.all()
  permissions_classes = [IsAuthenticated, IsAccountOwner]

  # Filters
  filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
  search_fields = ("title",)
  ordering_fields = ('title',)

  def dispatch(self, request, *args, **kwargs):
    """Verify users exists"""
    identification = kwargs["identification"]
    self.user = get_object_or_404(User, identification=identification)
    return super(UserDocumentsViewSet, self).dispatch(request, *args, **kwargs)

  def list(self, request, *args, **kwargs):
    documents = Documents.objects.filter(user=self.user)
    if "search" in request.query_params:
      documents = documents.filter(title__startswith=request.query_params["search"])
    data = DocumentsModelSerializer(documents, many=True).data
    return Response(data, status=status.HTTP_200_OK)

  def retrieve(self, request, *args, **kwargs):
    print(kwargs)
    document = Documents.objects.filter(
      user=self.user,
      title=kwargs["pk"]
    )
    data = DocumentsModelSerializer(document, many=True).data
    return Response(data, status=status.HTTP_200_OK)