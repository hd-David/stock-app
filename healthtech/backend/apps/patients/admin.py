"""Patient admin configuration."""
from django.contrib import admin
from .models import PatientProfile


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_type', 'insurance_provider', 'created_at']
    list_filter = ['blood_type']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'insurance_provider']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
