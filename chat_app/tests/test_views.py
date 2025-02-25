import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from chat_app.models import Chat
from chat_app.serializers import ChatSerializer

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
def test_chat_create_view(authenticated_client, test_user):
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

@pytest.mark.django_db
def test_chat_retrieve_view(authenticated_client, test_chat):
    url = reverse('chat-retrieve', kwargs={'pk': test_chat.id})

    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Test Chat'

@pytest.mark.django_db
def test_chat_retrieve_view_not_found(authenticated_client):
    url = reverse('chat-retrieve', kwargs={'pk': 999})

    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_chat_list_view(authenticated_client, test_chat):
    url = reverse('chat-list')

    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['name'] == 'Test Chat'

@pytest.mark.django_db
def test_chat_list_view_filtering(authenticated_client, test_user):
    Chat.objects.create(name='Chat 1', user=test_user)
    Chat.objects.create(name='Chat 2', user=test_user)

    url = reverse('chat-list')
    response = authenticated_client.get(url, {'user': test_user.id})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2

@pytest.mark.django_db
def test_chat_list_view_search(authenticated_client, test_user):
    Chat.objects.create(name='Chat 1', user=test_user)
    Chat.objects.create(name='Another Chat', user=test_user)

    url = reverse('chat-list')
    response = authenticated_client.get(url, {'search': 'Another'})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['name'] == 'Another Chat'


@pytest.mark.django_db
def test_chat_destroy_view(authenticated_client, test_chat):
    url = reverse('chat-destroy', kwargs={'pk': test_chat.id})

    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Chat.objects.filter(id=test_chat.id).exists()

@pytest.mark.django_db
def test_chat_destroy_view_unauthenticated(api_client, test_chat):
    url = reverse('chat-destroy', kwargs={'pk': test_chat.id})

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN