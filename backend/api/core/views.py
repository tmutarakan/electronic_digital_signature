from rest_framework import viewsets, permissions, pagination
from .serializers import (
    EmployeeSerializer,
    OrganizationSerializer,
    PositionSerializer,
    CivilDocumentSerializer,
    ElectronicDigitalSignatureSerializer,
)
from .models import (
    Employee,
    Organization,
    Position,
    CivilDocument,
    ElectronicDigitalSignature,
)


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    ordering = 'slug'


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


class CivilDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = CivilDocumentSerializer
    queryset = CivilDocument.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


class ElectronicDigitalSignatureViewSet(viewsets.ModelViewSet):
    serializer_class = ElectronicDigitalSignatureSerializer
    queryset = ElectronicDigitalSignature.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination
