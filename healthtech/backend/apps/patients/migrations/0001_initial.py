# Generated migration for patients app
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
            name='PatientProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='patient_profile',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('blood_type', models.CharField(
                    choices=[
                        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
                        ('unknown', 'Unknown'),
                    ],
                    default='unknown', max_length=10,
                )),
                ('height_cm', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('weight_kg', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('allergies', models.TextField(blank=True)),
                ('chronic_conditions', models.TextField(blank=True)),
                ('current_medications', models.TextField(blank=True)),
                ('family_history', models.TextField(blank=True)),
                ('insurance_provider', models.CharField(blank=True, max_length=200)),
                ('insurance_policy_number', models.CharField(blank=True, max_length=100)),
                ('insurance_group_number', models.CharField(blank=True, max_length=100)),
                ('insurance_expiry_date', models.DateField(blank=True, null=True)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=200)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=20)),
                ('emergency_contact_relationship', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'db_table': 'patient_profiles'},
        ),
    ]
