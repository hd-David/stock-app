# Generated migration for triage app
import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SymptomCheck',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('patient', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='symptom_checks',
                    to='patients.patientprofile',
                )),
                ('symptoms', models.JSONField()),
                ('symptom_duration', models.CharField(blank=True, max_length=100)),
                ('symptom_severity', models.IntegerField(default=5)),
                ('suggested_conditions', models.JSONField(default=list)),
                ('urgency_level', models.CharField(
                    choices=[
                        ('emergency', 'Emergency - Call 911'),
                        ('urgent', 'Urgent - See doctor today'),
                        ('soon', 'See doctor within 48 hours'),
                        ('routine', 'Schedule routine appointment'),
                    ],
                    max_length=20,
                )),
                ('recommendation', models.TextField()),
                ('additional_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'symptom_checks', 'ordering': ['-created_at']},
        ),
    ]
