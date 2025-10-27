from django.contrib import admin
from .models import UserProfile, InstructorFollow


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(InstructorFollow)
class InstructorFollowAdmin(admin.ModelAdmin):
    list_display = ['student', 'instructor', 'followed_at']
    list_filter = ['followed_at']
    search_fields = ['student__username', 'instructor__username']
    readonly_fields = ['followed_at']
