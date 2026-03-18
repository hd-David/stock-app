"""Telemedicine serializers."""
from rest_framework import serializers
from .models import TelemedicineSession, ChatMessage


class TelemedicineSessionSerializer(serializers.ModelSerializer):
    appointment_patient = serializers.CharField(
        source='appointment.patient.user.get_full_name', read_only=True
    )
    appointment_doctor = serializers.CharField(
        source='appointment.doctor.user.get_full_name', read_only=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = TelemedicineSession
        fields = [
            'id', 'appointment', 'appointment_patient', 'appointment_doctor',
            'status', 'status_display', 'room_name', 'access_token',
            'doctor_joined_at', 'patient_joined_at', 'started_at', 'ended_at',
            'duration_minutes', 'recording_url', 'notes', 'created_at',
        ]
        read_only_fields = [
            'id', 'room_name', 'access_token', 'doctor_joined_at', 'patient_joined_at',
            'started_at', 'ended_at', 'duration_minutes', 'created_at',
        ]


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'sender', 'sender_name', 'message', 'is_read', 'timestamp']
        read_only_fields = ['id', 'sender', 'is_read', 'timestamp']
