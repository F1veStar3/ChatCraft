from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Chat
from .serializers import ChatSerializer


class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]


class ChatRetrieveView(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def get_object(self):
        instance = super().get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("You are not allowed to view this chat room.")
        return instance


class ChatListView(ListAPIView):
    serializer_class = ChatSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)


class ChatDestroyView(DestroyAPIView):
    queryset = Chat.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this chat.")
        super().perform_destroy(instance)



