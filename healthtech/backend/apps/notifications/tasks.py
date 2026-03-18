"""Notification Celery tasks."""
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_email_notification(self, user_id: str, subject: str, message: str):
    """Send an email notification to a user."""
    try:
        from apps.users.models import CustomUser
        user = CustomUser.objects.get(id=user_id)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info(f"Email sent to {user.email}: {subject}")
    except Exception as exc:
        logger.error(f"Failed to send email to user {user_id}: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_sms_notification(self, phone_number: str, message: str):
    """Send an SMS notification via Twilio (stub if no credentials)."""
    twilio_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
    twilio_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
    twilio_from = getattr(settings, 'TWILIO_FROM_NUMBER', None)

    if not all([twilio_sid, twilio_token, twilio_from]):
        logger.info(f"[SMS STUB] To: {phone_number}, Message: {message}")
        return

    try:
        from twilio.rest import Client
        client = Client(twilio_sid, twilio_token)
        client.messages.create(body=message, from_=twilio_from, to=phone_number)
        logger.info(f"SMS sent to {phone_number}")
    except Exception as exc:
        logger.error(f"Failed to send SMS to {phone_number}: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task
def send_appointment_reminder(appointment_id: str):
    """Create notification and send email reminder for an appointment."""
    try:
        from apps.appointments.models import Appointment
        from apps.notifications.models import Notification

        appointment = Appointment.objects.select_related(
            'patient__user', 'doctor__user'
        ).get(id=appointment_id)

        patient_user = appointment.patient.user
        doctor_name = appointment.doctor.user.get_full_name()
        appt_time = appointment.date_time.strftime('%B %d, %Y at %I:%M %p UTC')

        title = "Appointment Reminder"
        message = (
            f"Reminder: You have an appointment with Dr. {doctor_name} "
            f"on {appt_time}. Please be on time."
        )

        Notification.objects.create(
            user=patient_user,
            notification_type='appointment_reminder',
            title=title,
            message=message,
        )

        send_email_notification.delay(str(patient_user.id), title, message)
        logger.info(f"Appointment reminder sent for appointment {appointment_id}")
    except Exception as exc:
        logger.error(f"Failed to send appointment reminder for {appointment_id}: {exc}")


@shared_task
def send_appointment_confirmation(appointment_id: str):
    """Create notification and send confirmation email for an appointment."""
    try:
        from apps.appointments.models import Appointment
        from apps.notifications.models import Notification

        appointment = Appointment.objects.select_related(
            'patient__user', 'doctor__user'
        ).get(id=appointment_id)

        patient_user = appointment.patient.user
        doctor_name = appointment.doctor.user.get_full_name()
        appt_time = appointment.date_time.strftime('%B %d, %Y at %I:%M %p UTC')

        title = "Appointment Confirmed"
        message = (
            f"Your appointment with Dr. {doctor_name} on {appt_time} has been confirmed. "
            f"Please arrive 10 minutes early."
        )

        Notification.objects.create(
            user=patient_user,
            notification_type='appointment_confirmed',
            title=title,
            message=message,
        )

        send_email_notification.delay(str(patient_user.id), title, message)
        logger.info(f"Appointment confirmation sent for appointment {appointment_id}")
    except Exception as exc:
        logger.error(f"Failed to send appointment confirmation for {appointment_id}: {exc}")
