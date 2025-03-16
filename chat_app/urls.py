from django.urls import path

from .views import ChatCreateView, ChatRetrieveView, ChatListView, ChatDestroyView

urlpatterns = [
    path('chats/create/1/', ChatCreateView.as_view(), name='chat-create'),
    path('chats/<int:pk>/', ChatRetrieveView.as_view(), name='chat-retrieve'),
    path('chats/', ChatListView.as_view(), name='chat-list'),
    path('chats/<int:pk>/delete/', ChatDestroyView.as_view(), name='chat-destroy'),
]
