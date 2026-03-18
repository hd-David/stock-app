"""Patient serializers."""
from rest_framework import serializers
from .models import PatientProfile


class PatientProfileSerializer(serializers.ModelSerializer):
    """Serializer for patient profile."""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = PatientProfile
        fields = [
            'id', 'user', 'user_email', 'user_full_name',
            'blood_type', 'height_cm', 'weight_kg',
            'allergies', 'chronic_conditions', 'current_medications', 'family_history',
            'insurance_provider', 'insurance_policy_number', 'insurance_group_number',
            'insurance_expiry_date',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
