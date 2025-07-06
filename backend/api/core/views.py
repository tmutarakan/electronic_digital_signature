from django.core.mail import send_mail
from rest_framework import permissions, pagination, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.settings.base import EMAIL_HOST_USER
from .serializers import RegisterSerializer, UserSerializer, ContactSerailizer


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"
    ordering = "slug"


class PingView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        tags=["core"],
        operation_summary="Проверка API",
        operation_description="Этот эндпоинт возвращает сообщение об успехе",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Успешный ответ",
                examples={"application/json": {"message": "pong"}},
            ),
            status.HTTP_404_NOT_FOUND: "Не найдено",
        },
    )
    def get(self, request):
        # Логика обработки GET запроса
        data = {"message": "pong"}
        return Response(data, status=status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        tags=["core"],
        operation_summary="Создание нового пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Имя пользователя"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Пароль"
                ),
                "password2": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Подтверждение пароля"
                ),
            },
            required=["username", "password", "password2"],
        ),
        responses={status.HTTP_201_CREATED: "Успешное создание"},
    )
    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            data={
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "Пользователь успешно создан",
            },
            status=status.HTTP_201_CREATED,
        )


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    @swagger_auto_schema(
        tags=["core"],
        operation_summary="Профиль",
        responses={status.HTTP_200_OK: "Успешный ответ"},
    )
    def get(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        return Response(
            {
                "user": UserSerializer(
                    request.user, context=self.get_serializer_context()
                ).data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=["core"],
        operation_summary="Выход из системы",
        responses={status.HTTP_200_OK: "Успешный ответ"},
    )
    def post(self, request):
        try:
            # Отзываем все токены пользователя
            for token in OutstandingToken.objects.filter(user=request.user):
                BlacklistedToken.objects.create(token=token)
            return Response(
                {"message": "Вы успешно вышли из системы"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerailizer

    @swagger_auto_schema(
        tags=["core"],
        operation_summary="Обратная связь",
        responses={status.HTTP_200_OK: "Успешный ответ"},
    )
    def post(
        self, request, *args, **kwargs  # pylint: disable=unused-argument
    ) -> Response | None:
        serializer_class = ContactSerailizer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get("name")
            from_email = data.get("email")
            subject = data.get("subject")
            message = data.get("message")
            send_mail(
                f"От {name} | {subject}",
                message,
                from_email,
                [EMAIL_HOST_USER],
            )
            return Response({"success": "Sent"}, status=status.HTTP_200_OK)
