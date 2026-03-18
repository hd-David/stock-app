"""Appointment serializers."""
from django.utils import timezone
from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for reading appointment data."""
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.get_specialization_display', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'doctor_specialization', 'date_time', 'duration_minutes',
            'status', 'appointment_type', 'reason', 'notes',
            'cancellation_reason', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating an appointment with slot conflict validation."""

    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'duration_minutes', 'appointment_type', 'reason']

    def validate_date_time(self, value):
        from datetime import timedelta as td
        # Require at least 5 minutes in the future to avoid race-condition edge cases
        if value < timezone.now() + td(minutes=5):
            raise serializers.ValidationError(
                "Appointment date/time must be at least 5 minutes in the future."
            )
        return value

    def validate(self, attrs):
        doctor = attrs['doctor']
        date_time = attrs['date_time']
        duration = attrs.get('duration_minutes', 30)

        from django.utils import timezone as tz
        from datetime import timedelta

        slot_end = date_time + timedelta(minutes=duration)

        # Check for overlapping appointments for the doctor
        overlapping = Appointment.objects.filter(
            doctor=doctor,
            status__in=['scheduled', 'confirmed'],
        ).exclude(id=self.instance.id if self.instance else None)

        for appt in overlapping:
            existing_end = appt.date_time + timedelta(minutes=appt.duration_minutes)
            if date_time < existing_end and slot_end > appt.date_time:
                raise serializers.ValidationError(
                    f"This slot conflicts with an existing appointment at {appt.date_time}."
                )
        return attrs

    def create(self, validated_data):
        patient = validated_data.pop('patient', None)
        if patient is None:
            raise serializers.ValidationError("Patient profile is required.")
        return Appointment.objects.create(patient=patient, **validated_data)


class AppointmentCancelSerializer(serializers.Serializer):
    """Serializer for cancelling an appointment."""
    cancellation_reason = serializers.CharField(required=False, allow_blank=True)
