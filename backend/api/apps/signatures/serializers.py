from rest_framework import serializers
from .models import Sertificate, ElectronicDigitalSignature, CertificationCenter


class CertificationCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificationCenter
        fields = ["name", "inn"]
        read_only_fields = ["name", "inn"]
        swagger_schema_fields = {
            "description": "Центры сертификации",
        }


class SertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sertificate
        fields = [
            "file",
            "position",
            "certification_center",
            "start_date",
            "end_date",
        ]
        read_only_fields = ["file", "position", "certification_center", "start_date", "end_date"]
        swagger_schema_fields = {
            "description": "Сертификаты",
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["position"] = instance.position.name
        representation["certification_center"] = instance.certification_center.name
        return representation


class ElectronicDigitalSignatureSerializer(serializers.ModelSerializer):
    sertificate = SertificateSerializer(read_only=True)

    class Meta:
        model = ElectronicDigitalSignature
        fields = ["archive", "start_date", "end_date", "sertificate"]
        read_only_fields = ["archive", "start_date", "end_date", "sertificate"]
        swagger_schema_fields = {
            "description": "Электронные цифровые подписи",
        }
