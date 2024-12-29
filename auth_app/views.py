from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

import requests

@api_view(['GET'])
def google_login(request):
    auth_url = (
        f"{settings.GOOGLE_AUTH_URI}?"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=email profile"
    )
    return redirect(auth_url)

@api_view(['GET'])
def google_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Authorization code not provided'}, status=400)

    token_response = requests.post(
        settings.GOOGLE_TOKEN_URI,
        data={
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code',
        },
    )

    if token_response.status_code != 200:
        return JsonResponse({'error': 'Failed to obtain token'}, status=400)

    token_data = token_response.json()
    access_token = token_data.get('access_token')

    userinfo_response = requests.get(
        settings.GOOGLE_USERINFO_URI,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    if userinfo_response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch user info'}, status=400)

    userinfo = userinfo_response.json()
    email = userinfo.get('email')
    name = userinfo.get('name')

    user, created = User.objects.get_or_create(username=email, defaults={'email': email, 'first_name': name})

    return JsonResponse({
        'message': 'User logged in' if not created else 'User registered',
        'email': user.email,
        'name': user.first_name,
    })