"""Doctor profile models."""
import uuid
from django.db import models
from apps.users.models import CustomUser


SPECIALIZATION_CHOICES = [
    ('general', 'General Practice'),
    ('cardiology', 'Cardiology'),
    ('dermatology', 'Dermatology'),
    ('endocrinology', 'Endocrinology'),
    ('gastroenterology', 'Gastroenterology'),
    ('neurology', 'Neurology'),
    ('oncology', 'Oncology'),
    ('orthopedics', 'Orthopedics'),
    ('pediatrics', 'Pediatrics'),
    ('psychiatry', 'Psychiatry'),
    ('pulmonology', 'Pulmonology'),
    ('radiology', 'Radiology'),
    ('surgery', 'Surgery'),
    ('urology', 'Urology'),
    ('other', 'Other'),
]

DAY_CHOICES = [
    (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
    (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday'),
]


class DoctorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, default='general')
    license_number = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_accepting_patients = models.BooleanField(default=True)
    languages_spoken = models.CharField(max_length=200, default='English')
    education = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'doctor_profiles'

    def __str__(self) -> str:
        return f"Dr. {self.user.get_full_name()} ({self.get_specialization_display()})"


class DoctorAvailability(models.Model):
    """Doctor weekly availability schedule."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    slot_duration_minutes = models.PositiveIntegerField(default=30)

    class Meta:
        db_table = 'doctor_availability'
        unique_together = ['doctor', 'day_of_week']

    def __str__(self) -> str:
        return f"{self.doctor} - {self.get_day_of_week_display()}: {self.start_time}-{self.end_time}"
