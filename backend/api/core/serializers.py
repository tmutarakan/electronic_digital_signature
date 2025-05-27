from rest_framework import serializers
from .models import (
    Employee,
    Organization,
    Position,
    Passport,
    INN,
    SNILS,
    Sertificate,
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


class SertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sertificate
        fields = "__all__"


class ElectronicDigitalSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronicDigitalSignature
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class ContactSerailizer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()

    def create(self, validated_data):
        # Since this is a simple serializer, just return the validated data
        return validated_data

    def update(self, instance, validated_data):
        # Since this is a simple serializer, just update the instance dict
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance
