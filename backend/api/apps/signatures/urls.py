from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CertificateViewSet,
    ElectronicDigitalSignatureViewSet,
    CertificationCenterViewSet,
)

router = DefaultRouter()

router.register("certificate", CertificateViewSet, basename="certificate")
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
