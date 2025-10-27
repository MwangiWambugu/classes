from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    # room_name captured from URL; use a safe pattern
    re_path(r"ws/chat/(?P<room_name>[\w-]+)/$", consumer.ChatConsumer.as_asgi()),
]
