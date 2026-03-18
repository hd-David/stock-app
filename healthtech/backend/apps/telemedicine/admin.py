"""Telemedicine admin configuration."""
from django.contrib import admin
from .models import TelemedicineSession, ChatMessage


@admin.register(TelemedicineSession)
class TelemedicineSessionAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'status', 'room_name', 'started_at', 'ended_at', 'duration_minutes']
    list_filter = ['status']
    search_fields = [
        'appointment__patient__user__email', 'appointment__doctor__user__email', 'room_name'
    ]
    readonly_fields = ['id', 'room_name', 'access_token', 'created_at']
    ordering = ['-created_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'session', 'timestamp', 'is_read']
    list_filter = ['is_read']
    search_fields = ['sender__email', 'message']
    readonly_fields = ['id', 'timestamp']
    ordering = ['-timestamp']
