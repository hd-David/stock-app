"""Telemedicine session models."""
import uuid
import secrets
from django.db import models
from apps.appointments.models import Appointment
from apps.users.models import CustomUser


class TelemedicineSession(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('ended', 'Ended'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='telemedicine_session')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    room_name = models.CharField(max_length=100, unique=True)
    access_token = models.CharField(max_length=256, blank=True)
    doctor_joined_at = models.DateTimeField(null=True, blank=True)
    patient_joined_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    recording_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'telemedicine_sessions'

    def save(self, *args, **kwargs):
        if not self.room_name:
            self.room_name = f"room_{secrets.token_urlsafe(16)}"
        if not self.access_token:
            self.access_token = secrets.token_urlsafe(64)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Session for {self.appointment}"


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(TelemedicineSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_messages'
        ordering = ['timestamp']

    def __str__(self) -> str:
        return f"Message from {self.sender} in {self.session}"
