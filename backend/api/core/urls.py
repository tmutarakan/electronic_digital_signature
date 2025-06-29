from django.urls import path
from .views import (
    PingView,
    RegisterView,
    ProfileView,
    FeedBackView,
)

urlpatterns = [
    path('ping/', PingView.as_view(), name='ping'),
    path("feedback/", FeedBackView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view()),
]
