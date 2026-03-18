"""User admin configuration."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin panel configuration for CustomUser."""
    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'is_mfa_enabled', 'is_active']
    list_filter = ['role', 'is_active', 'is_mfa_enabled', 'is_staff']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone_number']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = UserAdmin.fieldsets + (
        ('HealthTech Info', {
            'fields': (
                'role', 'phone_number', 'date_of_birth', 'profile_picture',
                'is_mfa_enabled', 'totp_secret', 'created_at', 'updated_at',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('HealthTech Info', {
            'fields': ('email', 'role', 'phone_number', 'first_name', 'last_name'),
        }),
    )
