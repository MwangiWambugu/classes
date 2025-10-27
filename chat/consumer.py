import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Channel, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract room name from URL
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = f"chat_{self.room_name}"

        # Join the channel group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        print(f"✅ Connected to room: {self.room_name}")

    async def disconnect(self, close_code):
        # Leave the group when disconnected
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"❌ Disconnected from room: {self.room_name}")

    async def receive(self, text_data=None, bytes_data=None):
        """
        Handle message received from WebSocket client.
        """
        if not text_data:
            return

        data = json.loads(text_data)
        message = data.get("message")
        username = data.get("username") or "Anonymous"

        if not message.strip():
            return

        # Save message to the database
        msg_obj = await self.save_message(username, self.room_name, message)

        # Broadcast message to everyone in the room
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": msg_obj["content"],
                "username": msg_obj["username"],
                "timestamp": msg_obj["timestamp"],
            },
        )

    async def chat_message(self, event):
        """
        Receive message from the group and send it to WebSocket.
        """
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "username": event["username"],
                    "timestamp": event["timestamp"],
                }
            )
        )

    @database_sync_to_async
    def save_message(self, username, room_name, message):
        """
        Save message to the DB synchronously inside async context.
        """
        channel, _ = Channel.objects.get_or_create(name=room_name)

        # Optional: check if username exists in auth users
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        msg = Message.objects.create(
            channel=channel,
            user=username if not user else user.username,  # handles str or object
            content=message,
        )

        return {
            "id": msg.id,
            "username": user.username if user else username or "Anonymous",
            "content": msg.content,
            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
