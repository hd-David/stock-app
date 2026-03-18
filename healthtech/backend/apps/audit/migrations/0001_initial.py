# Generated migration for audit app
import uuid
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL,
                )),
                ('action', models.CharField(
                    choices=[
                        ('CREATE', 'Create'), ('READ', 'Read'), ('UPDATE', 'Update'), ('DELETE', 'Delete'),
                        ('LOGIN', 'Login'), ('LOGOUT', 'Logout'), ('FAILED_LOGIN', 'Failed Login'),
                        ('PASSWORD_RESET', 'Password Reset'), ('MFA_ENABLE', 'MFA Enable'),
                        ('FILE_UPLOAD', 'File Upload'), ('FILE_DOWNLOAD', 'File Download'),
                    ],
                    max_length=20,
                )),
                ('resource', models.CharField(max_length=100)),
                ('resource_id', models.CharField(blank=True, max_length=100)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True)),
                ('request_method', models.CharField(blank=True, max_length=10)),
                ('request_path', models.CharField(blank=True, max_length=500)),
                ('response_status', models.IntegerField(blank=True, null=True)),
                ('details', models.JSONField(default=dict)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'audit_logs', 'ordering': ['-timestamp']},
        ),
    ]
