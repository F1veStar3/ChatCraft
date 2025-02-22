import pytest
from django.contrib.auth.models import User

from chat_app.models import Chat, Message
from chat_app.serializers import ChatSerializer, MessageSerializer


@pytest.mark.django_db
def test_message_serializer():
    user = User.objects.create_user(username='testuser', password='12345')
    chat = Chat.objects.create(name='Test Chat', user=user)

    message = Message.objects.create(
        chat=chat,
        user_message='Hello, world!',
        assistant_message='Hi there!'
    )

    serializer = MessageSerializer(message)
    data = serializer.data

    assert data['id'] == message.id
    assert data['chat'] == chat.id
    assert data['user_message'] == 'Hello, world!'
    assert data['assistant_message'] == 'Hi there!'
    assert 'created_at' in data


@pytest.mark.django_db
def test_message_deserializer():
    user = User.objects.create_user(username='testuser', password='12345')
    chat = Chat.objects.create(name='Test Chat', user=user)

    message_data = {
        'chat': chat.id,
        'user_message': 'Hello, world!',
        'assistant_message': 'Hi there!'
    }

    serializer = MessageSerializer(data=message_data)
    assert serializer.is_valid(), serializer.errors

    message = serializer.save()

    assert message.chat == chat
    assert message.user_message == 'Hello, world!'
    assert message.assistant_message == 'Hi there!'


@pytest.mark.django_db
def test_message_serializer_invalid_data():
    invalid_data = {
        'user_message': 'Hello, world!',
        'assistant_message': 'Hi there!'
    }

    serializer = MessageSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'chat' in serializer.errors


@pytest.mark.django_db
def test_chat_serializer():
    user = User.objects.create_user(username='testuser', password='12345')

    chat = Chat.objects.create(name='Test Chat', user=user)

    serializer = ChatSerializer(chat)
    data = serializer.data

    assert data['id'] == chat.id
    assert data['name'] == 'Test Chat'
    assert data['user'] == user.id
    assert 'created_at' in data


@pytest.mark.django_db
def test_chat_deserializer():
    user = User.objects.create_user(username='testuser', password='12345')

    chat_data = {
        'name': 'Test Chat',
        'user': user.id
    }

    serializer = ChatSerializer(data=chat_data)
    assert serializer.is_valid(), serializer.errors

    chat = serializer.save()

    assert chat.name == 'Test Chat'
    assert chat.user == user


@pytest.mark.django_db
def test_chat_serializer_invalid_data():
    invalid_data = {
        'name': 'Test Chat'
    }

    serializer = ChatSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'user' in serializer.errors
