from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Employee


class EmplyeeCreateAPITestCase(APITestCase):
    def setUp(self):
        #self.employees = [{}]
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        url = reverse("token")
        resp = self.client.post(
            url, {"username": "testuser", "password": "testpassword"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in resp.data)
        token = resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        #self.employee = Employee.objects.create()

    def test_get_empoyee_list(self):
        """
        Тест получение списка сотрудников
        """
        url = reverse("employees:employee-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), dict)
        self.assertTrue("results" in response.data)
        self.assertIsInstance(response.json()["results"], list)
