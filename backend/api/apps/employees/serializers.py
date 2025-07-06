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
        read_only_fields = ["series", "number", "date_of_issue", "birthdate", "birthplace", "code"]
        swagger_schema_fields = {
            "description": "Паспорт",
        }


class INNSerializer(serializers.ModelSerializer):
    class Meta:
        model = INN
        fields = ["value"]
        read_only_fields = ["value"]
        swagger_schema_fields = {
            "description": "ИНН",
        }


class SNILSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNILS
        fields = ["value"]
        read_only_fields = ["value"]
        swagger_schema_fields = {
            "description": "СНИЛС",
        }


class EmployeeSerializer(serializers.ModelSerializer):
    signatures = ElectronicDigitalSignatureSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ["surname", "name", "patronymic", "signatures"]
        read_only_fields = ["surname", "name", "patronymic", "signatures"]
        swagger_schema_fields = {
            "description": "Сотрудники",
        }
