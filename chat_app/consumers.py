import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.shortcuts import get_object_or_404
from openai import OpenAI

from .models import Chat, Message
from .serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_message = text_data_json['user_message']

        chat = await self.get_chat(self.chat_id)

        previous_messages = await self.get_previous_messages(chat)
        messages_history = [{"role": "system", "content": "You are a helpful assistant"}]

        for msg in previous_messages:
            messages_history.append({"role": "user", "content": msg.user_message})
            if msg.assistant_message:
                messages_history.append({"role": "assistant", "content": msg.assistant_message})

        messages_history.append({"role": "user", "content": user_message})

        client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages_history,
            stream=False
        )

        assistant_message = response.choices[0].message.content

        await self.save_message(chat, user_message, assistant_message)

        await self.send(text_data=json.dumps({
            'assistant_message': assistant_message
        }))

    @sync_to_async
    def get_chat(self, chat_id):
        return get_object_or_404(Chat, id=chat_id)

    @sync_to_async
    def get_previous_messages(self, chat):
        return list(Message.objects.filter(chat=chat).order_by('created_at'))

    @sync_to_async
    def save_message(self, chat, user_message, assistant_message):
        serializer = MessageSerializer(data={
            'chat': chat.id,
            'user_message': user_message,
            'assistant_message': assistant_message
        })
        if serializer.is_valid():
            print("Serializer is valid. Saving message...")
            serializer.save(chat=chat)
        else:
            print("Serializer errors:", serializer.errors)
