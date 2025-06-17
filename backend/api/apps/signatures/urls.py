from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SertificateViewSet,
    ElectronicDigitalSignatureViewSet,
    CertificationCenterViewSet,
)

router = DefaultRouter()

router.register("sertificate", SertificateViewSet, basename="sertificate")
router.register(
    "electronic-digital-signature",
    ElectronicDigitalSignatureViewSet,
    basename="electronic-digital-signature",
)
router.register(
    "certification-center",
    CertificationCenterViewSet,
    basename="certification-center",
)

urlpatterns = [
    path("", include(router.urls)),
]
