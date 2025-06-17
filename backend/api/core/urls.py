from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    FeedBackView,
)

urlpatterns = [
    path("feedback/", FeedBackView.as_view()),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
]
