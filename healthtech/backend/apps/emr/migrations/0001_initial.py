# Generated migration for emr app
import uuid
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import apps.emr.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
        ('doctors', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('patient', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='medical_records',
                    to='patients.patientprofile',
                )),
                ('doctor', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='medical_records',
                    to='doctors.doctorprofile',
                )),
                ('visit_date', models.DateField()),
                ('chief_complaint', models.TextField()),
                ('diagnosis', models.TextField()),
                ('treatment_plan', models.TextField()),
                ('notes', models.TextField(blank=True)),
                ('follow_up_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'db_table': 'medical_records', 'ordering': ['-visit_date']},
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('record', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='prescriptions',
                    to='emr.medicalrecord',
                )),
                ('medication_name', models.CharField(max_length=200)),
                ('dosage', models.CharField(max_length=100)),
                ('frequency', models.CharField(
                    choices=[
                        ('once', 'Once Daily'), ('twice', 'Twice Daily'), ('thrice', 'Three Times Daily'),
                        ('four', 'Four Times Daily'), ('as_needed', 'As Needed'), ('weekly', 'Weekly'),
                    ],
                    max_length=20,
                )),
                ('duration_days', models.PositiveIntegerField()),
                ('instructions', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'db_table': 'prescriptions'},
        ),
        migrations.CreateModel(
            name='LabResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('record', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='lab_results',
                    to='emr.medicalrecord',
                )),
                ('test_name', models.CharField(max_length=200)),
                ('result_value', models.TextField()),
                ('reference_range', models.CharField(blank=True, max_length=200)),
                ('is_abnormal', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, null=True, upload_to=apps.emr.models.lab_result_path)),
                ('test_date', models.DateField()),
                ('notes', models.TextField(blank=True)),
            ],
            options={'db_table': 'lab_results'},
        ),
        migrations.CreateModel(
            name='MedicalDocument',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('record', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='documents',
                    to='emr.medicalrecord',
                )),
                ('title', models.CharField(max_length=200)),
                ('document_type', models.CharField(
                    choices=[
                        ('report', 'Medical Report'), ('prescription', 'Prescription'),
                        ('lab', 'Lab Result'), ('imaging', 'Imaging'),
                        ('referral', 'Referral'), ('consent', 'Consent Form'), ('other', 'Other'),
                    ],
                    default='other', max_length=20,
                )),
                ('file', models.FileField(upload_to=apps.emr.models.medical_document_path)),
                ('uploaded_by', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL,
                )),
                ('description', models.TextField(blank=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'medical_documents'},
        ),
    ]
