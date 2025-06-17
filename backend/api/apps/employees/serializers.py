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
        fields = "__all__"


class INNSerializer(serializers.ModelSerializer):
    class Meta:
        model = INN
        fields = "__all__"


class SNILSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNILS
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    signatures = ElectronicDigitalSignatureSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = "__all__"
