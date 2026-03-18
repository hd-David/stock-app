"""Triage/symptom checker models."""
import uuid
from django.db import models
from apps.patients.models import PatientProfile


class SymptomCheck(models.Model):
    URGENCY_CHOICES = [
        ('emergency', 'Emergency - Call 911'),
        ('urgent', 'Urgent - See doctor today'),
        ('soon', 'See doctor within 48 hours'),
        ('routine', 'Schedule routine appointment'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='symptom_checks')
    symptoms = models.JSONField()  # List of symptom strings
    symptom_duration = models.CharField(max_length=100, blank=True)
    symptom_severity = models.IntegerField(default=5)  # 1-10 scale
    suggested_conditions = models.JSONField(default=list)  # List of possible conditions
    urgency_level = models.CharField(max_length=20, choices=URGENCY_CHOICES)
    recommendation = models.TextField()
    additional_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'symptom_checks'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Symptom check for {self.patient} at {self.created_at}"
