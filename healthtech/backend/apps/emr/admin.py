"""EMR admin configuration."""
from django.contrib import admin
from .models import MedicalRecord, Prescription, LabResult, MedicalDocument


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'visit_date', 'diagnosis', 'follow_up_date']
    list_filter = ['visit_date']
    search_fields = [
        'patient__user__email', 'patient__user__first_name', 'doctor__user__email',
        'diagnosis', 'chief_complaint',
    ]
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-visit_date']
    date_hierarchy = 'visit_date'


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['medication_name', 'dosage', 'frequency', 'duration_days', 'is_active']
    list_filter = ['frequency', 'is_active']
    search_fields = ['medication_name', 'record__patient__user__email']
    readonly_fields = ['id']


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ['test_name', 'test_date', 'is_abnormal', 'result_value']
    list_filter = ['is_abnormal', 'test_date']
    search_fields = ['test_name', 'record__patient__user__email']
    readonly_fields = ['id']


@admin.register(MedicalDocument)
class MedicalDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document_type', 'uploaded_by', 'uploaded_at']
    list_filter = ['document_type']
    search_fields = ['title', 'record__patient__user__email']
    readonly_fields = ['id', 'uploaded_at']
