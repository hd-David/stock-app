# Generated migration for notifications app
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
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='notifications',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('notification_type', models.CharField(
                    choices=[
                        ('appointment_reminder', 'Appointment Reminder'),
                        ('appointment_confirmed', 'Appointment Confirmed'),
                        ('appointment_cancelled', 'Appointment Cancelled'),
                        ('prescription_ready', 'Prescription Ready'),
                        ('lab_result_ready', 'Lab Result Ready'),
                        ('message', 'Message'),
                        ('system', 'System'),
                    ],
                    max_length=30,
                )),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'notifications', 'ordering': ['-created_at']},
        ),
    ]
