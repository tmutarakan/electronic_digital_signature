from rest_framework import viewsets
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


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    lookup_field = "id"


class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    lookup_field = "id"


class CivilDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = CivilDocumentSerializer
    queryset = CivilDocument.objects.all()
    lookup_field = "id"


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    lookup_field = "id"


class ElectronicDigitalSignatureViewSet(viewsets.ModelViewSet):
    serializer_class = ElectronicDigitalSignatureSerializer
    queryset = ElectronicDigitalSignature.objects.all()
    lookup_field = "id"
