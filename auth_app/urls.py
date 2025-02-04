from django.urls import path, include
from .views import GoogleLoginAPIView, GoogleCallbackAPIView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path("google/login/", GoogleLoginAPIView.as_view(), name="google-login"),
    path("google/callback/", GoogleCallbackAPIView.as_view(), name="google-callback"),
]