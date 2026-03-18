"""Doctor serializers."""
from rest_framework import serializers
from .models import DoctorProfile, DoctorAvailability


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = DoctorAvailability
        fields = [
            'id', 'day_of_week', 'day_name', 'start_time', 'end_time',
            'is_available', 'slot_duration_minutes',
        ]
        read_only_fields = ['id']


class DoctorProfileSerializer(serializers.ModelSerializer):
    """Serializer for doctor profile."""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    availability = DoctorAvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            'id', 'user', 'user_email', 'user_full_name',
            'specialization', 'specialization_display', 'license_number',
            'bio', 'years_of_experience', 'consultation_fee',
            'is_accepting_patients', 'languages_spoken',
            'education', 'certifications', 'availability',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class DoctorProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating doctor profile."""

    class Meta:
        model = DoctorProfile
        fields = [
            'specialization', 'license_number', 'bio', 'years_of_experience',
            'consultation_fee', 'is_accepting_patients', 'languages_spoken',
            'education', 'certifications',
        ]
