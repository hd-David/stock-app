# Generated migration for appointments app
import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('patient', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='appointments',
                    to='patients.patientprofile',
                )),
                ('doctor', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='appointments',
                    to='doctors.doctorprofile',
                )),
                ('date_time', models.DateTimeField()),
                ('duration_minutes', models.PositiveIntegerField(default=30)),
                ('status', models.CharField(
                    choices=[
                        ('scheduled', 'Scheduled'), ('confirmed', 'Confirmed'),
                        ('cancelled', 'Cancelled'), ('completed', 'Completed'), ('no_show', 'No Show'),
                    ],
                    default='scheduled', max_length=20,
                )),
                ('appointment_type', models.CharField(
                    choices=[('in_person', 'In Person'), ('telemedicine', 'Telemedicine')],
                    default='in_person', max_length=20,
                )),
                ('reason', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('cancellation_reason', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'db_table': 'appointments', 'ordering': ['-date_time']},
        ),
    ]
