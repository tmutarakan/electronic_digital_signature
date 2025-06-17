from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet,
    PassportViewSet,
    INNViewSet,
    SNILSViewSet,
)

router = DefaultRouter()
router.register("employee", EmployeeViewSet, basename="employee")
router.register("passport", PassportViewSet, basename="passport")
router.register("inn", INNViewSet, basename="inn")
router.register("snils", SNILSViewSet, basename="snils")


urlpatterns = [
    path("", include(router.urls)),
]
