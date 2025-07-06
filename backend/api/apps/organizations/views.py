from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions
from core.views import PageNumberSetPagination
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    OrganizationSerializer,
    PositionSerializer,
)
from .models import (
    Organization,
    Position,
)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["Организации"],
        operation_summary="Организации",
        operation_description="Возвращает список организаций",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["Организации"],
        operation_summary="Организации",
        operation_description="Создаёт запись о организации",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["Организации"],
        operation_summary="Организации",
        operation_description="Возвращает конкретную запись о организации",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["Организации"],
        operation_summary="Организации",
        operation_description="Изменяет запись о организации",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=["Организации"],
        operation_summary="Организации",
        operation_description="Изменяет часть записи о организации",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["Организации"],
        operation_summary="Организации",
        operation_description="Удаляет запись о организации",
    ),
)
class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberSetPagination


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["Должности"],
        operation_summary="Должности",
        operation_description="Возвращает список должностей",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["Должности"],
        operation_summary="Должности",
        operation_description="Создаёт запись о должности",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["Должности"],
        operation_summary="Должности",
        operation_description="Возвращает конкретную запись о должности",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["Должности"],
        operation_summary="Должности",
        operation_description="Изменяет запись о должности",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=["Должности"],
        operation_summary="Должности",
        operation_description="Изменяет часть записи о должности",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["Должности"],
        operation_summary="Должности",
        operation_description="Удаляет запись о должности",
    ),
)
class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberSetPagination
