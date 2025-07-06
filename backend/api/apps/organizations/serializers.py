from rest_framework import serializers
from .models import (
    Organization,
    Position,
)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["name", "ogrn", "inn", "kpp", "registered_address"]
        read_only_fields = ["name", "ogrn", "inn", "kpp", "registered_address"]
        swagger_schema_fields = {
            "description": "Организации",
        }


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["name", "organization"]
        read_only_fields = ["name", "organization"]
        swagger_schema_fields = {
            "description": "Должности",
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["organization"] = instance.organization.name
        return representation
