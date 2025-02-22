import pytest
from django.contrib.auth.models import User

from chat_app.models import Chat, Message


@pytest.mark.django_db
def test_chat_creation():
    user = User.objects.create_user(username='testuser', password='12345')

    chat = Chat.objects.create(name='Test Chat', user=user)

    assert chat.name == 'Test Chat'
    assert chat.user.username == 'testuser'
    assert chat.created_at is not None


@pytest.mark.django_db
def test_message_creation():
    user = User.objects.create_user(username='testuser', password='12345')

    chat = Chat.objects.create(name='Test Chat', user=user)

    message = Message.objects.create(
        chat=chat,
        user_message='Hello, world!',
        assistant_message='Hi there!'
    )
    assert message.chat.name == 'Test Chat'
    assert message.user_message == 'Hello, world!'
    assert message.assistant_message == 'Hi there!'
    assert message.created_at is not None


@pytest.mark.django_db
def test_chat_str_method():
    user = User.objects.create_user(username='testuser', password='12345')
    chat = Chat.objects.create(name='Test Chat', user=user)
    assert str(chat) == f"Chat {chat.id} by testuser"


@pytest.mark.django_db
def test_message_str_method():
    user = User.objects.create_user(username='testuser', password='12345')
    chat = Chat.objects.create(name='Test Chat', user=user)
    message = Message.objects.create(chat=chat, user_message='Hello, world!')
    assert str(message) == f"Message {message.id} by testuser"
