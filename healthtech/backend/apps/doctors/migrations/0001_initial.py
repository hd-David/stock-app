# Generated migration for doctors app
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
            name='DoctorProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='doctor_profile',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('specialization', models.CharField(
                    choices=[
                        ('general', 'General Practice'), ('cardiology', 'Cardiology'),
                        ('dermatology', 'Dermatology'), ('endocrinology', 'Endocrinology'),
                        ('gastroenterology', 'Gastroenterology'), ('neurology', 'Neurology'),
                        ('oncology', 'Oncology'), ('orthopedics', 'Orthopedics'),
                        ('pediatrics', 'Pediatrics'), ('psychiatry', 'Psychiatry'),
                        ('pulmonology', 'Pulmonology'), ('radiology', 'Radiology'),
                        ('surgery', 'Surgery'), ('urology', 'Urology'), ('other', 'Other'),
                    ],
                    default='general', max_length=50,
                )),
                ('license_number', models.CharField(max_length=100, unique=True)),
                ('bio', models.TextField(blank=True)),
                ('years_of_experience', models.PositiveIntegerField(default=0)),
                ('consultation_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_accepting_patients', models.BooleanField(default=True)),
                ('languages_spoken', models.CharField(default='English', max_length=200)),
                ('education', models.TextField(blank=True)),
                ('certifications', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'db_table': 'doctor_profiles'},
        ),
        migrations.CreateModel(
            name='DoctorAvailability',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('doctor', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='availability',
                    to='doctors.doctorprofile',
                )),
                ('day_of_week', models.IntegerField(
                    choices=[
                        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
                        (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday'),
                    ],
                )),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('slot_duration_minutes', models.PositiveIntegerField(default=30)),
            ],
            options={'db_table': 'doctor_availability', 'unique_together': {('doctor', 'day_of_week')}},
        ),
    ]
