from django.contrib import admin

# Register your models here.

from .models import Channel, Message


# admin.site.register(Channel)
# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('id','channel','user','created_at')
#     list_filter = ('channel','created_at')

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel', 'user', 'content', 'timestamp')
    list_filter = ('channel', 'timestamp')