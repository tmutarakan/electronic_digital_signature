from rest_framework import serializers
from .models import (
    Employee,
    Position,
    Sertificate,
    ElectronicDigitalSignature,
)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"


class SertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sertificate
        fields = "__all__"


class ElectronicDigitalSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronicDigitalSignature
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    signatures = ElectronicDigitalSignatureSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = "__all__"
