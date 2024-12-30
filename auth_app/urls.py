from django.urls import path
from .views import GoogleLoginAPIView, GoogleCallbackAPIView

urlpatterns = [
    path("google/login/", GoogleLoginAPIView.as_view(), name="google-login"),
    path("google/callback/", GoogleCallbackAPIView.as_view(), name="google-callback"),
]