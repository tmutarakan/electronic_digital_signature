import pytest
from django.urls import reverse
from rest_framework import status
from .factories import EmployeeFactory


pytestmark = pytest.mark.django_db


class TestEmplyeeCRUD:
    employee_list_url = reverse("employees:employee-list")

    def test_create_employee_without_auth(self, api_client):
        data = {
            "surname": "Иванов",
            "name": "Ивае",
            "patronymic": "Иванович",
            "gender": "М",
            "passport": "123",
            "inn": "123",
            "snils": "123",
        }
        response = api_client.post(self.employee_list_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_employee(self, api_client):
        EmployeeFactory.create_batch(5)
        response = api_client.get(self.employee_list_url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["results"]) == 5

    def test_delete_employee_without_auth(self, api_client):
        employee = EmployeeFactory()
        url = reverse("employees:employee-detail", kwargs={"slug": employee.slug})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_employee_without_auth(self, api_client):
        employee = EmployeeFactory()
        data = {
            "surname": "Иванов",
            "name": "Ивае",
            "patronymic": "Иванович",
            "gender": "М",
            "passport": "123",
            "inn": "123",
            "snils": "123",
        }
        url = reverse("employees:employee-detail", kwargs={"slug": employee.slug})
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
