"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from core.views import LogoutView

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="🚀 EDS API",  # Название вашего API
        default_version="v1",  # Версия API
        description="API для нашего проекта",  # Краткое описание
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@yourapp.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Кому разрешён доступ к документации
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('swagger/v1/', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/v1/', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.yaml', schema_view_v1.without_ui(cache_timeout=0), name='schema-yaml'),
    path('swagger.json', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    path("api/v1/", include("core.urls")),
    path(
        "api/v1/", include(("apps.employees.urls", "employees"), namespace="employees")
    ),
    path(
        "api/v1/",
        include(
            ("apps.organizations.urls", "organizations"), namespace="organizations"
        ),
    ),
    # path("api/v1/", include('apps.signatures.urls')),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token"),
    path("api/v1/refresh_token/", TokenRefreshView.as_view(), name="refresh_token"),
    path("api/v1/logout/", LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:  # Только для режима разработки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
