"""Electronic Medical Records models."""
import uuid
import os
from django.db import models
from apps.patients.models import PatientProfile
from apps.doctors.models import DoctorProfile
from apps.users.models import CustomUser


def medical_document_path(instance, filename: str) -> str:
    """Generate secure file upload path."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('medical_documents', str(instance.record.patient.id), filename)


def lab_result_path(instance, filename: str) -> str:
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('lab_results', str(instance.record.patient.id), filename)


class MedicalRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='medical_records')
    visit_date = models.DateField()
    chief_complaint = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    notes = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'medical_records'
        ordering = ['-visit_date']

    def __str__(self) -> str:
        return f"Record for {self.patient} on {self.visit_date}"


class Prescription(models.Model):
    FREQUENCY_CHOICES = [
        ('once', 'Once Daily'),
        ('twice', 'Twice Daily'),
        ('thrice', 'Three Times Daily'),
        ('four', 'Four Times Daily'),
        ('as_needed', 'As Needed'),
        ('weekly', 'Weekly'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    duration_days = models.PositiveIntegerField()
    instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'prescriptions'

    def __str__(self) -> str:
        return f"{self.medication_name} for {self.record.patient}"


class LabResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='lab_results')
    test_name = models.CharField(max_length=200)
    result_value = models.TextField()
    reference_range = models.CharField(max_length=200, blank=True)
    is_abnormal = models.BooleanField(default=False)
    file = models.FileField(upload_to=lab_result_path, null=True, blank=True)
    test_date = models.DateField()
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'lab_results'

    def __str__(self) -> str:
        return f"{self.test_name} for {self.record.patient}"


class MedicalDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('report', 'Medical Report'),
        ('prescription', 'Prescription'),
        ('lab', 'Lab Result'),
        ('imaging', 'Imaging'),
        ('referral', 'Referral'),
        ('consent', 'Consent Form'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='other')
    file = models.FileField(upload_to=medical_document_path)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'medical_documents'

    def __str__(self) -> str:
        return f"{self.title} - {self.record.patient}"
