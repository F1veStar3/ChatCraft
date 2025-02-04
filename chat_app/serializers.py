from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Chat, Message

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat', 'user_message', 'assistant_message', 'created_at']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id','name', 'user', 'created_at']
