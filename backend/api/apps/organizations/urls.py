from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrganizationViewSet,
    PositionViewSet,
)

router = DefaultRouter()

router.register("organization", OrganizationViewSet, basename="organization")
router.register("position", PositionViewSet, basename="position")


urlpatterns = [
    path("", include(router.urls)),
]
