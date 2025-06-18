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


class INNViewSet(viewsets.ModelViewSet):
    serializer_class = INNSerializer
    queryset = INN.objects.all()
    lookup_field = "slug"


class SNILSViewSet(viewsets.ModelViewSet):
    serializer_class = SNILSSerializer
    queryset = SNILS.objects.all()
    lookup_field = "slug"


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["surname", "name", "patronymic"]
    ordering_fields = ["surname", "name", "patronymic"]
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination
