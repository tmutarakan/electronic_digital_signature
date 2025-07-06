from django.utils.decorators import method_decorator
from rest_framework import viewsets, filters, permissions
from core.views import PageNumberSetPagination
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    EmployeeSerializer,
    PassportSerializer,
    INNSerializer,
    SNILSSerializer,
)
from .models import (
    Employee,
    Passport,
    INN,
    SNILS,
)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["Паспорт"],
        operation_summary="Паспорт",
        operation_description="Возвращает список паспортов",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["Паспорт"],
        operation_summary="Паспорт",
        operation_description="Создаёт запись о паспорте",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["Паспорт"],
        operation_summary="Паспорт",
        operation_description="Возвращает конкретную запись о паспорте",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["Паспорт"],
        operation_summary="Паспорт",
        operation_description="Изменяет запись о паспорте",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=["Паспорт"],
        operation_summary="Паспорт",
        operation_description="Изменяет часть записи о паспорте",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["Паспорт"],
        operation_summary="Паспорт",
        operation_description="Удаляет запись о паспорте",
    ),
)
class PassportViewSet(viewsets.ModelViewSet):
    serializer_class = PassportSerializer
    queryset = Passport.objects.all()
    lookup_field = "slug"


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["ИНН"],
        operation_summary="ИНН",
        operation_description="Возвращает список ИНН",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["ИНН"],
        operation_summary="ИНН",
        operation_description="Создаёт запись о ИНН",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["ИНН"],
        operation_summary="ИНН",
        operation_description="Возвращает конкретную запись о ИНН",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["ИНН"],
        operation_summary="ИНН",
        operation_description="Изменяет запись о ИНН",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=["ИНН"],
        operation_summary="ИНН",
        operation_description="Изменяет часть записи о ИНН",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["ИНН"],
        operation_summary="ИНН",
        operation_description="Удаляет запись о ИНН",
    ),
)
class INNViewSet(viewsets.ModelViewSet):
    serializer_class = INNSerializer
    queryset = INN.objects.all()
    lookup_field = "slug"


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["СНИЛС"],
        operation_summary="СНИЛС",
        operation_description="Возвращает список СНИЛС",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["СНИЛС"],
        operation_summary="СНИЛС",
        operation_description="Создаёт запись о СНИЛС",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["СНИЛС"],
        operation_summary="СНИЛС",
        operation_description="Возвращает конкретную запись о СНИЛС",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["СНИЛС"],
        operation_summary="СНИЛС",
        operation_description="Изменяет запись о СНИЛС",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=["СНИЛС"],
        operation_summary="СНИЛС",
        operation_description="Изменяет часть записи о СНИЛС",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["СНИЛС"],
        operation_summary="СНИЛС",
        operation_description="Удаляет запись о СНИЛС",
    ),
)
class SNILSViewSet(viewsets.ModelViewSet):
    serializer_class = SNILSSerializer
    queryset = SNILS.objects.all()
    lookup_field = "slug"


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["Сотрудники"],
        operation_summary="Сотрудники",
        operation_description="Возвращает список сотрудников",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["Сотрудники"],
        operation_summary="Сотрудники",
        operation_description="Создаёт запись о сотруднике",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["Сотрудники"],
        operation_summary="Сотрудники",
        operation_description="Возвращает конкретную запись о сотруднике",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["Сотрудники"],
        operation_summary="Сотрудники",
        operation_description="Изменяет запись о сотруднике",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=["Сотрудники"],
        operation_summary="Сотрудники",
        operation_description="Изменяет часть записи о сотруднике",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["Сотрудники"],
        operation_summary="Сотрудники",
        operation_description="Удаляет запись о сотруднике",
    ),
)
class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["surname", "name", "patronymic"]
    ordering_fields = ["surname", "name", "patronymic"]
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination
