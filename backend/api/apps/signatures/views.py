from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions
from core.views import PageNumberSetPagination
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    CertificateSerializer,
    ElectronicDigitalSignatureSerializer,
    CertificationCenterSerializer,
)
from .models import Certificate, ElectronicDigitalSignature, CertificationCenter


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["Сертификаты"],
        operation_summary="Сертификаты",
        operation_description="Возвращает список сертификатов",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["Сертификаты"],
        operation_summary="Сертификаты",
        operation_description="Создаёт запись о сертификате",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["Сертификаты"],
        operation_summary="Сертификаты",
        operation_description="Возвращает конкретную запись о сертификате",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["Сертификаты"],
        operation_summary="Сертификаты",
        operation_description="Изменяет запись о сертификате",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=["Сертификаты"],
        operation_summary="Сертификаты",
        operation_description="Изменяет часть записи о сертификате",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["Сертификаты"],
        operation_summary="Сертификаты",
        operation_description="Удаляет запись о сертификате",
    ),
)
class CertificateViewSet(viewsets.ModelViewSet):
    serializer_class = CertificateSerializer
    queryset = Certificate.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination

@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["Электронные подписи"],
        operation_summary="Электронные подписи",
        operation_description="Возвращает список электронных подписей",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["Электронные подписи"],
        operation_summary="Электронные подписи",
        operation_description="Создаёт запись о электронной подписи",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["Электронные подписи"],
        operation_summary="Электронные подписи",
        operation_description="Возвращает конкретную запись о электронной подписи",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["Электронные подписи"],
        operation_summary="Электронные подписи",
        operation_description="Изменяет запись о электронной подписи",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=["Электронные подписи"],
        operation_summary="Электронные подписи",
        operation_description="Изменяет часть записи о электронной подписи",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["Электронные подписи"],
        operation_summary="Электронные подписи",
        operation_description="Удаляет запись о электронной подписи",
    ),
)
class ElectronicDigitalSignatureViewSet(viewsets.ModelViewSet):
    serializer_class = ElectronicDigitalSignatureSerializer
    queryset = ElectronicDigitalSignature.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["Центры сертификации"],
        operation_summary="Центры сертификации",
        operation_description="Возвращает список центров сертификации",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["Центры сертификации"],
        operation_summary="Центры сертификации",
        operation_description="Создаёт запись о центре сертификации",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["Центры сертификации"],
        operation_summary="Центры сертификации",
        operation_description="Возвращает конкретную запись о центре сертификации",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["Центры сертификации"],
        operation_summary="Центры сертификации",
        operation_description="Изменяет запись о центре сертификации",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=["Центры сертификации"],
        operation_summary="Центры сертификации",
        operation_description="Изменяет часть записи о центре сертификации",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["Центры сертификации"],
        operation_summary="Центры сертификации",
        operation_description="Удаляет запись о центре сертификации",
    ),
)
class CertificationCenterViewSet(viewsets.ModelViewSet):
    serializer_class = CertificationCenterSerializer
    queryset = CertificationCenter.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination
