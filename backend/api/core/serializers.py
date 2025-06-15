from django.contrib.auth.models import User
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


class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


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
    signatures = ElectronicDigitalSignatureSerializer(many=True, read_only=True)
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
