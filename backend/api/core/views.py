from rest_framework import permissions, pagination, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from django.core.mail import send_mail
from .serializers import RegisterSerializer, UserSerializer, ContactSerailizer


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "Пользователь успешно создан",
            }
        )


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        return Response(
            {
                "user": UserSerializer(
                    request.user, context=self.get_serializer_context()
                ).data,
            }
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Отзываем все токены пользователя
            for token in OutstandingToken.objects.filter(user=request.user):
                BlacklistedToken.objects.create(token=token)
            return Response({"message": "Вы успешно вышли из системы"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"
    ordering = "slug"


class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerailizer

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
            return Response({"success": "Sent"})
