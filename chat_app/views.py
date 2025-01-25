from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView

from .models import Chat
from .serializers import ChatSerializer


class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class ChatRetrieveView(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = 'pk'


class ChatListView(ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class ChatDestroyView(DestroyAPIView):
    queryset = Chat.objects.all()
    lookup_field = 'pk'
