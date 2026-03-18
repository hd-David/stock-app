"""Appointment admin configuration."""
from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date_time', 'status', 'appointment_type', 'duration_minutes']
    list_filter = ['status', 'appointment_type']
    search_fields = [
        'patient__user__email', 'patient__user__first_name', 'patient__user__last_name',
        'doctor__user__email', 'doctor__user__first_name', 'doctor__user__last_name',
    ]
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-date_time']
    date_hierarchy = 'date_time'
