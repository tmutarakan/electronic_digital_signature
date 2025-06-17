from rest_framework import viewsets, permissions
from core.views import PageNumberSetPagination
from .serializers import (
    OrganizationSerializer,
    PositionSerializer,
)
from .models import (
    Organization,
    Position,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination
