import requests
from django.conf import settings
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import UpdateProfileSerializer


class GoogleLoginAPIView(APIView):
    def get(self, request):
        google_auth_url = (
            "https://accounts.google.com/o/oauth2/auth"
            "?response_type=code"
            f"&client_id={settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
            "&scope=openid%20email%20profile"
        )

        return Response({"auth_url": google_auth_url}, status=status.HTTP_200_OK)


class GoogleCallbackAPIView(APIView):
    def get(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response({"error": "Authorization code not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange code for access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        token_response = requests.post(token_url, data=token_data)
        if token_response.status_code != 200:
            return Response({"error": "Failed to obtain token"}, status=status.HTTP_400_BAD_REQUEST)

        tokens = token_response.json()
        access_token = tokens.get("access_token")

        # Get user info
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        user_info_response = requests.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"})
        if user_info_response.status_code != 200:
            return Response({"error": "Failed to fetch user info"}, status=status.HTTP_400_BAD_REQUEST)

        user_info = user_info_response.json()
        email = user_info.get("email")
        name = user_info.get("name")

        if not email:
            return Response({"error": "Email not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Create or get user
        user, created = User.objects.get_or_create(username=email, defaults={"email": email, "first_name": name})

        return Response({
            "message": "Authentication successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.first_name,
            }
        }, status=status.HTTP_200_OK)


class UpdateProfileLogoView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UpdateProfileSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'user'

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'logo',
                openapi.IN_FORM,
                description="file upload",
                type=openapi.TYPE_FILE,
                required=True
            )
        ]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
