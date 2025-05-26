from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet,
    OrganizationViewSet,
    PositionViewSet,
    PassportViewSet,
    INNViewSet,
    SNILSViewSet,
    SertificateViewSet,
    ElectronicDigitalSignatureViewSet,
)

router = DefaultRouter()
router.register("employee", EmployeeViewSet, basename="employee")
router.register("organization", OrganizationViewSet, basename="organization")
router.register("position", PositionViewSet, basename="position")
router.register("passport", PassportViewSet, basename="passport")
router.register("inn", INNViewSet, basename="inn")
router.register("snils", SNILSViewSet, basename="snils")
router.register("sertificate", SertificateViewSet, basename="sertificate")
router.register(
    "electronic-digital-signature",
    ElectronicDigitalSignatureViewSet,
    basename="electronic-digital-signature",
)

urlpatterns = [path("", include(router.urls))]
