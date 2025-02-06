# import pytest
# from django.contrib.auth.models import User
# from .models import Chat, Message
#
# @pytest.mark.django_db
# def test_chat_creation():
#     user = User.objects.create(username='testuser', password='testpass123')
#
#     chat = Chat.objects.create(name='Test Chat', user=user)
#
#     assert chat.name == 'Test Chat'
#     assert chat.user == user
#     assert chat.created_at is not None
#
#     assert str(chat) == f"Chat {chat.id} by {user.username}"
#
# @pytest.mark.django_db
# def test_message_creation():
#     user = User.objects.create(username='testuser', password='testpass123')
#     chat = Chat.objects.create(name='Test Chat', user=user)
#
#     message = Message.objects.create(
#         chat=chat,
#         user_message='Hello, world!',
#         assistant_message='Hi there!'
#     )
#
#     assert message.chat == chat
#     assert message.user_message == 'Hello, world!'
#     assert message.assistant_message == 'Hi there!'
#     assert message.created_at is not None
#
#     assert str(message) == f"Message {message.id} by {user.username}"
#
# @pytest.mark.django_db
# def test_chat_messages_relationship():
#     user = User.objects.create(username='testuser', password='testpass123')
#     chat = Chat.objects.create(name='Test Chat', user=user)
#
#     message1 = Message.objects.create(chat=chat, user_message='Message 1')
#     message2 = Message.objects.create(chat=chat, user_message='Message 2')
#
#     assert chat.messages.count() == 2
#     assert message1 in chat.messages.all()
#     assert message2 in chat.messages.all()