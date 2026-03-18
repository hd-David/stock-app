"""Doctor admin configuration."""
from django.contrib import admin
from .models import DoctorProfile, DoctorAvailability


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'license_number', 'years_of_experience',
                    'consultation_fee', 'is_accepting_patients']
    list_filter = ['specialization', 'is_accepting_patients']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'license_number']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day_of_week', 'start_time', 'end_time', 'is_available', 'slot_duration_minutes']
    list_filter = ['day_of_week', 'is_available']
    search_fields = ['doctor__user__email', 'doctor__user__first_name', 'doctor__user__last_name']
    readonly_fields = ['id']
