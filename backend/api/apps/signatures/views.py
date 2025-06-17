from rest_framework import viewsets
from core.views import PageNumberSetPagination
from .serializers import (
    SertificateSerializer,
    ElectronicDigitalSignatureSerializer,
    CertificationCenterSerializer,
)
from .models import Sertificate, ElectronicDigitalSignature, CertificationCenter


class SertificateViewSet(viewsets.ModelViewSet):
    serializer_class = SertificateSerializer
    queryset = Sertificate.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


class ElectronicDigitalSignatureViewSet(viewsets.ModelViewSet):
    serializer_class = ElectronicDigitalSignatureSerializer
    queryset = ElectronicDigitalSignature.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


class CertificationCenterViewSet(viewsets.ModelViewSet):
    serializer_class = CertificationCenterSerializer
    queryset = CertificationCenter.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination
