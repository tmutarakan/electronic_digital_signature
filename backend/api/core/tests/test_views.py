from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class PingAPITestCase(TestCase):
    def test_ping_endpoint_returns_pong(self):
        """
        Тест для проверки эндпоинта /api/v1/ping/
        """
        # Генерируем URL на основе имени маршрута
        url = reverse("ping")

        # Отправляем GET-запрос на эндпоинт
        response = self.client.get(url)

        # Проверяем статус ответа (должен быть 200 OK)
        self.assertEqual(response.status_code, 200)

        # Проверяем содержимое JSON-ответа
        self.assertEqual(response.json(), {"message": "pong"})


class UserCreateAPITestCase(APITestCase):
    def test_create_user_success(self):
        """
        Тест успешного создания пользователя
        """
        url = reverse("register")
        data = {
            "username": "john_doe",
            "password": "PXXsR|uLBK%UlxRx",
            "password2": "PXXsR|uLBK%UlxRx",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "user": {"username": "john_doe"},
                "message": "Пользователь успешно создан",
            },
        )

    def test_create_user_missing_username(self):
        """
        Тест ошибки при отсутствии имени пользователя
        """
        url = reverse("register")
        data = {"password": "PXXsR|uLBK%UlxRx", "password2": "PXXsR|uLBK%UlxRx"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"username": ["Обязательное поле."]})

    def test_create_user_passwords_not_match(self):
        """
        Тест пароли не совпадают
        """
        url = reverse("register")
        data = {
            "username": "john_doe",
            "password": "PXXsR|uLBK%UlxRx",
            "password2": "pxxSr uLBK%UlxRx",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': 'Пароли не совпадают'})
