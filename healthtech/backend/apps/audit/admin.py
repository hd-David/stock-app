"""Audit admin configuration."""
from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'resource', 'resource_id', 'ip_address',
                    'request_method', 'response_status', 'timestamp']
    list_filter = ['action', 'request_method', 'response_status']
    search_fields = ['user__email', 'resource', 'request_path', 'ip_address']
    readonly_fields = [f.name for f in AuditLog._meta.get_fields()]
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
