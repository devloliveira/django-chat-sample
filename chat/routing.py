from django.urls import re_path

from . import consumers

# Specific for the chat room. This file defines the websocket path and ties it
# to a specific consumer (a python class)
websocket_urlpatterns = [
    re_path(r'ws/chat/room/(?P<room_name>\w+)$', consumers.ChatConsumer.as_asgi()),
]