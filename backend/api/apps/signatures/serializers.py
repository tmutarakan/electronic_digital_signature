from rest_framework import serializers
from .models import Sertificate, ElectronicDigitalSignature, CertificationCenter


class CertificationCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificationCenter
        fields = "__all__"


class SertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sertificate
        fields = [
            "filename",
            "file",
            "position",
            "certification_center",
            "start_date",
            "end_date",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["position"] = instance.position.name
        representation["certification_center"] = instance.certification_center.name
        return representation


class ElectronicDigitalSignatureSerializer(serializers.ModelSerializer):
    sertificate = SertificateSerializer(read_only=True)

    class Meta:
        model = ElectronicDigitalSignature
        fields = ["filename", "archive", "start_date", "end_date", "sertificate"]
