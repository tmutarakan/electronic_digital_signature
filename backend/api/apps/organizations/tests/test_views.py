import pytest
from django.urls import reverse
from rest_framework import status
from .factories import OrganizationFactory, PositionFactory

pytestmark = pytest.mark.django_db


class TestOrganizationCRUD:
    organization_list_url = reverse("organizations:organization-list")

    def test_create_organization_without_auth(self, api_client):
        data = {
            "name": "New Organization",
            "ogrn": "1234567890123",
            "inn": "1234567890",
            "kpp": "123456789",
            "registered_address": "123 Main St",
        }

        response = api_client.post(self.organization_list_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # assert response.status_code == status.HTTP_201_CREATED

        # returned_json = response.json()
        # assert "id" in returned_json
        # assert returned_json["name"] == data["name"]
        # assert returned_json["ogrn"] == data["ogrn"]
        # assert returned_json["inn"] == data["inn"]
        # assert returned_json["kpp"] == data["kpp"]
        # assert returned_json["registered_address"] == data["registered_address"]

    def test_retrieve_organizations(self, api_client):
        OrganizationFactory.create_batch(5)
        response = api_client.get(self.organization_list_url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert len(data["results"]) == 5

    def test_delete_organization_without_auth(self, api_client):
        organization = OrganizationFactory()
        url = reverse(
            "organizations:organization-detail", kwargs={"slug": organization.slug}
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_update_organization_without_auth(self, api_client):
        organization = OrganizationFactory()
        data = {
            "name": "New name",
            "ogrn": "1234567890123",
            "inn": "1234567890",
            "kpp": "123456789",
            "registered_address": "123 Main St",
        }
        url = reverse(
            "organizations:organization-detail", kwargs={"slug": organization.slug}
        )

        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # assert response.status_code == status.HTTP_200_OK

        # returned_json = response.json()
        # assert returned_json["name"] == data["name"]
        # assert returned_json["ogrn"] == data["ogrn"]
        # assert returned_json["inn"] == data["inn"]
        # assert returned_json["kpp"] == data["kpp"]
        # assert returned_json["registered_address"] == data["registered_address"]


class TestPositionCRUD:
    position_list_url = reverse("organizations:position-list")

    def test_create_position_without_auth(self, api_client):
        data = {
            "name": "New Position",
            "organization": "1234567890123",
        }

        response = api_client.post(self.position_list_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_positions(self, api_client):
        PositionFactory.create_batch(5)
        response = api_client.get(self.position_list_url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert len(data["results"]) == 5

    def test_delete_position_without_auth(self, api_client):
        position = PositionFactory()
        url = reverse("organizations:position-detail", kwargs={"slug": position.slug})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_position_without_auth(self, api_client):
        position = PositionFactory()
        data = {
            "name": "New name",
            "organization": "1234567890123",
        }
        url = reverse("organizations:position-detail", kwargs={"slug": position.slug})

        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
