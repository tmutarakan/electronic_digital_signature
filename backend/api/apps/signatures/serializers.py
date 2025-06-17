from rest_framework import serializers
from .models import (
    Sertificate,
    ElectronicDigitalSignature,
    CertificationCenter
)



class SertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sertificate
        fields = "__all__"


class ElectronicDigitalSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronicDigitalSignature
        fields = "__all__"

class CertificationCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificationCenter
        fields = "__all__"