from django.urls import path
from ChatApp.consumers import ChatConsumer,PersonalChatConsumer

websocket_urlpatterns = [
    path('ws/notification/<str:room_name>/', ChatConsumer.as_asgi()),
    path('ws/<int:id>/',PersonalChatConsumer.as_asgi()),
]