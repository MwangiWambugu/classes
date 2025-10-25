from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # channel_name captured from URL; use a safe pattern
    re_path(r"ws/chat/(?P<channel_name>[\w-]+)/$", consumers.ChatConsumer.as_asgi()),
]
