import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from chat_app.models import Chat


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(username='testuser', password='12345')


@pytest.fixture
def authenticated_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def test_chat(test_user):
    return Chat.objects.create(name='Test Chat', user=test_user)


@pytest.mark.django_db
def test_chat_create_view_authenticated(authenticated_client, test_user):
    url = reverse('chat-create')
    data = {'name': 'New Chat', 'user': test_user.id}

    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Chat.objects.filter(name='New Chat').exists()


@pytest.mark.django_db
def test_chat_create_view_unauthenticated(api_client):
    url = reverse('chat-create')
    data = {'name': 'New Chat'}

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


# Тести для ChatRetrieveView
@pytest.mark.django_db
def test_chat_retrieve_view_authenticated(authenticated_client, test_chat):
    url = reverse('chat-retrieve', kwargs={'pk': test_chat.id})

    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Test Chat'


@pytest.mark.django_db
def test_chat_retrieve_view_unauthenticated(api_client, test_chat):
    url = reverse('chat-retrieve', kwargs={'pk': test_chat.id})

    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_chat_destroy_view_authenticated(authenticated_client, test_chat):
    url = reverse('chat-destroy', kwargs={'pk': test_chat.id})

    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Chat.objects.filter(id=test_chat.id).exists()


@pytest.mark.django_db
def test_chat_destroy_view_unauthenticated(api_client, test_chat):
    url = reverse('chat-destroy', kwargs={'pk': test_chat.id})

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
