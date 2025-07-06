from rest_framework import serializers
from .models import (
    Organization,
    Position,
)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["name", "ogrn", "inn", "kpp", "registered_address"]

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["name", "organization"]
