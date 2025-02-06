from django.urls import path, include
from .views import GoogleLoginAPIView, GoogleCallbackAPIView, UpdateProfileLogoView

urlpatterns = [
    path('profile/update/<int:user>/', UpdateProfileLogoView.as_view(), name='update-profile-logo'),
    path("google/login/", GoogleLoginAPIView.as_view(), name="google-login"),
    path("google/callback/", GoogleCallbackAPIView.as_view(), name="google-callback"),
]