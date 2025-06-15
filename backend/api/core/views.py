from rest_framework import viewsets, permissions, pagination, filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from django.core.mail import send_mail
from api.settings import EMAIL_HOST_USER
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    EmployeeSerializer,
    OrganizationSerializer,
    PositionSerializer,
    PassportSerializer,
    INNSerializer,
    SNILSSerializer,
    SertificateSerializer,
    ElectronicDigitalSignatureSerializer,
    ContactSerailizer,
)
from .models import (
    Employee,
    Organization,
    Position,
    Passport,
    INN,
    SNILS,
    Sertificate,
    ElectronicDigitalSignature,
)


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
    page_size = 10
    page_size_query_param = "page_size"
    ordering = "slug"


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class PassportViewSet(viewsets.ModelViewSet):
    serializer_class = PassportSerializer
    queryset = Passport.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


class INNViewSet(viewsets.ModelViewSet):
    serializer_class = INNSerializer
    queryset = INN.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


class SNILSViewSet(viewsets.ModelViewSet):
    serializer_class = SNILSSerializer
    queryset = SNILS.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


class EmployeeViewSet(viewsets.ModelViewSet):
    search_fields = ["surname", "name", "patronymic"]
    filter_backends = (filters.SearchFilter,)
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


class SertificateViewSet(viewsets.ModelViewSet):
    serializer_class = SertificateSerializer
    queryset = Sertificate.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


class ElectronicDigitalSignatureViewSet(viewsets.ModelViewSet):
    serializer_class = ElectronicDigitalSignatureSerializer
    queryset = ElectronicDigitalSignature.objects.all()
    lookup_field = "slug"
    pagination_class = PageNumberSetPagination


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
