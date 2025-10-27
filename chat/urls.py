# authentication/urls.py
from django.urls import path
from chat.views import create_channel, channel_room, channels_list
from . import views


urlpatterns = [
    path("", views.home, name="home"),  # split-screen page
    path("create-channel/", views.create_channel, name="create_channel"),
    path("chat/<str:room_name>/", views.channel_room, name="channel_room"),
    path("channels-list/", views.channels_list, name="channels_list"),  # optional
    path("api/messages/<str:room_name>/", views.api_messages, name="api_messages"),

]