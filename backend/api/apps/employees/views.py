from rest_framework import viewsets, filters
from core.views import PageNumberSetPagination
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


class PassportViewSet(viewsets.ModelViewSet):
    serializer_class = PassportSerializer
    queryset = Passport.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


class INNViewSet(viewsets.ModelViewSet):
    serializer_class = INNSerializer
    queryset = INN.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


class SNILSViewSet(viewsets.ModelViewSet):
    serializer_class = SNILSSerializer
    queryset = SNILS.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


class EmployeeViewSet(viewsets.ModelViewSet):
    search_fields = ["surname", "name", "patronymic"]
    filter_backends = (filters.SearchFilter,)
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination
