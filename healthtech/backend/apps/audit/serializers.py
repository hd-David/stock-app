"""Audit log serializer."""
from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True, default=None)
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_email', 'action', 'action_display',
            'resource', 'resource_id', 'ip_address', 'user_agent',
            'request_method', 'request_path', 'response_status',
            'details', 'timestamp',
        ]
        read_only_fields = fields
