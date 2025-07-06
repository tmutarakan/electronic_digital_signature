from rest_framework import serializers
from apps.signatures.serializers import ElectronicDigitalSignatureSerializer
from .models import (
    Employee,
    Passport,
    INN,
    SNILS,
)


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = ["series", "number", "date_of_issue", "birthdate", "birthplace", "code"]


class INNSerializer(serializers.ModelSerializer):
    class Meta:
        model = INN
        fields = ["value"]


class SNILSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNILS
        fields = ["value"]


class EmployeeSerializer(serializers.ModelSerializer):
    signatures = ElectronicDigitalSignatureSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ["surname", "name", "patronymic", "signatures", "slug"]
