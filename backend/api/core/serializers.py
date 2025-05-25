from rest_framework import serializers
from .models import (
    Employee,
    Organization,
    Position,
    CivilDocument,
    ElectronicDigitalSignature,
)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"


class CivilDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CivilDocument
        fields = "__all__"


class ElectronicDigitalSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronicDigitalSignature
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
