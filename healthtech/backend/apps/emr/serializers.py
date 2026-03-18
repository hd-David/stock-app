"""EMR serializers."""
from django.conf import settings
from rest_framework import serializers
from .models import MedicalRecord, Prescription, LabResult, MedicalDocument

ALLOWED_FILE_TYPES = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']
ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png']


def validate_file(file):
    """Validate file size and type."""
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise serializers.ValidationError(
            f"File size must not exceed {settings.MAX_UPLOAD_SIZE // (1024 * 1024)}MB."
        )
    ext = file.name.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise serializers.ValidationError(
            f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}."
        )
    return file


class PrescriptionSerializer(serializers.ModelSerializer):
    frequency_display = serializers.CharField(source='get_frequency_display', read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id', 'record', 'medication_name', 'dosage', 'frequency',
            'frequency_display', 'duration_days', 'instructions', 'is_active',
        ]
        read_only_fields = ['id']


class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = [
            'id', 'record', 'test_name', 'result_value', 'reference_range',
            'is_abnormal', 'file', 'test_date', 'notes',
        ]
        read_only_fields = ['id']

    def validate_file(self, value):
        if value:
            return validate_file(value)
        return value


class MedicalDocumentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)

    class Meta:
        model = MedicalDocument
        fields = [
            'id', 'record', 'title', 'document_type', 'document_type_display',
            'file', 'uploaded_by', 'uploaded_by_name', 'description', 'uploaded_at',
        ]
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at']

    def validate_file(self, value):
        return validate_file(value)


class MedicalRecordSerializer(serializers.ModelSerializer):
    """Full medical record with nested prescriptions, lab results, and documents."""
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    lab_results = LabResultSerializer(many=True, read_only=True)
    documents = MedicalDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'visit_date', 'chief_complaint', 'diagnosis', 'treatment_plan',
            'notes', 'follow_up_date',
            'prescriptions', 'lab_results', 'documents',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MedicalRecordCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a medical record."""

    class Meta:
        model = MedicalRecord
        fields = [
            'patient', 'visit_date', 'chief_complaint',
            'diagnosis', 'treatment_plan', 'notes', 'follow_up_date',
        ]
