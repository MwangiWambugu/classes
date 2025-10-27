from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from chat.models import Channel, Message

# Shows the split-screen chat interface
def home(request):
    # Fetch all channels
    channels = Channel.objects.all().order_by('name')

    # Determine which channel is currently open (via ?room_name= param)
    room = request.GET.get("room_name")
    if room:
        current = get_object_or_404(Channel, name=room)
    else:
        current = channels.first()  # default to first channel

    # Get messages for the current channel
    messages = Message.objects.filter(channel=current).order_by("timestamp") if current else []

    context = {
        "channels": channels,
        "current": current,
        "messages": messages,
        "hide_search": True,
    }
    return render(request, "chat/chat_split.html", context)


# Handles new channel creation
def create_channel(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name", "").strip().replace(" ", "_")
        if room_name:
            channel, _ = Channel.objects.get_or_create(name=room_name)
            # Redirect back to home with new channel open
            return redirect(f"/chat/?room_name={channel.name}")
    return redirect("home")


# Optional — if you want a standalone chat room page
def channel_room(request, room_name):
    channel = get_object_or_404(Channel, name=room_name)
    messages = Message.objects.filter(channel=channel).order_by("timestamp")
    return render(request, "chat/chat_split.html", {
        "channels": Channel.objects.all().order_by('name'),
        "current": channel,
        "messages": messages,
        "hide_search": True,
    })


# Optional separate endpoint if you ever want a pure list view
def channels_list(request):
    channels = Channel.objects.all().order_by('name')
    return render(request, "chat/channels.html", {
        "channels": channels,
        "hide_search": True,
    })


def api_messages(request, room_name):
    channel = get_object_or_404(Channel, name=room_name)
    messages = Message.objects.filter(channel=channel).order_by("timestamp")
    return JsonResponse({
        "messages": [
            {
                "username": msg.user if isinstance(msg.user, str) else getattr(msg.user, "username", "Anonymous"),
                "content": msg.content,
                "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for msg in messages
        ]
    })