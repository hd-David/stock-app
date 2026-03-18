"""Triage admin configuration."""
from django.contrib import admin
from .models import SymptomCheck


@admin.register(SymptomCheck)
class SymptomCheckAdmin(admin.ModelAdmin):
    list_display = ['patient', 'urgency_level', 'symptom_severity', 'symptom_duration', 'created_at']
    list_filter = ['urgency_level']
    search_fields = ['patient__user__email', 'patient__user__first_name', 'patient__user__last_name']
    readonly_fields = ['id', 'suggested_conditions', 'urgency_level', 'recommendation', 'created_at']
    ordering = ['-created_at']
