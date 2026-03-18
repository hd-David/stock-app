"""Appointment views."""
import logging
from datetime import timedelta
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patients.models import PatientProfile
from apps.doctors.models import DoctorProfile
from apps.users.permissions import IsPatient, IsDoctor, IsDoctorOrAdmin
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer, AppointmentCancelSerializer

logger = logging.getLogger(__name__)


class AppointmentListCreateView(APIView):
    """List appointments (filtered by role) or create a new appointment."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == 'patient':
            try:
                patient = PatientProfile.objects.get(user=user)
                qs = Appointment.objects.filter(patient=patient).select_related(
                    'doctor__user', 'patient__user'
                )
            except PatientProfile.DoesNotExist:
                qs = Appointment.objects.none()
        elif user.role == 'doctor':
            try:
                doctor = DoctorProfile.objects.get(user=user)
                qs = Appointment.objects.filter(doctor=doctor).select_related(
                    'doctor__user', 'patient__user'
                )
            except DoctorProfile.DoesNotExist:
                qs = Appointment.objects.none()
        else:
            # admin/nurse sees all
            qs = Appointment.objects.select_related('doctor__user', 'patient__user').all()

        # Filter by status if provided
        appt_status = request.query_params.get('status')
        if appt_status:
            qs = qs.filter(status=appt_status)

        serializer = AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'patient':
            return Response(
                {'detail': 'Only patients can book appointments.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            patient = PatientProfile.objects.get(user=request.user)
        except PatientProfile.DoesNotExist:
            return Response(
                {'detail': 'Patient profile not found. Please complete your profile first.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AppointmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save(patient=patient)
            return Response(
                AppointmentSerializer(appointment).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetailView(APIView):
    """Retrieve, confirm, cancel, or complete a specific appointment."""
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            appt = Appointment.objects.select_related('doctor__user', 'patient__user').get(id=pk)
        except Appointment.DoesNotExist:
            return None

        if user.role == 'patient':
            if not hasattr(user, 'patient_profile') or appt.patient.user != user:
                return None
        elif user.role == 'doctor':
            if not hasattr(user, 'doctor_profile') or appt.doctor.user != user:
                return None
        return appt

    def get(self, request, pk):
        appt = self.get_object(pk, request.user)
        if not appt:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(AppointmentSerializer(appt).data)

    def patch(self, request, pk):
        """Update notes or confirm/complete by doctor."""
        appt = self.get_object(pk, request.user)
        if not appt:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        allowed_fields = ['notes']
        if request.user.role in ['doctor', 'admin', 'nurse']:
            allowed_fields += ['status']

        data = {k: v for k, v in request.data.items() if k in allowed_fields}
        serializer = AppointmentSerializer(appt, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentCancelView(APIView):
    """Cancel an appointment."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            appt = Appointment.objects.get(id=pk)
        except Appointment.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 'patient':
            if not hasattr(request.user, 'patient_profile') or appt.patient.user != request.user:
                return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        elif request.user.role == 'doctor':
            if not hasattr(request.user, 'doctor_profile') or appt.doctor.user != request.user:
                return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        if appt.status in ['cancelled', 'completed']:
            return Response(
                {'detail': f'Cannot cancel a {appt.status} appointment.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AppointmentCancelSerializer(data=request.data)
        if serializer.is_valid():
            appt.status = 'cancelled'
            appt.cancellation_reason = serializer.validated_data.get('cancellation_reason', '')
            appt.save(update_fields=['status', 'cancellation_reason', 'updated_at'])
            return Response(AppointmentSerializer(appt).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentCompleteView(APIView):
    """Mark appointment as completed (doctor only)."""
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]

    def post(self, request, pk):
        try:
            appt = Appointment.objects.get(id=pk)
        except Appointment.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 'doctor' and appt.doctor.user != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        if appt.status != 'confirmed':
            return Response(
                {'detail': 'Only confirmed appointments can be marked as completed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appt.status = 'completed'
        appt.save(update_fields=['status', 'updated_at'])
        return Response(AppointmentSerializer(appt).data)


class DoctorCalendarView(APIView):
    """Get appointments for a doctor filtered by date range."""
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]

    def get(self, request, pk):
        try:
            doctor = DoctorProfile.objects.get(id=pk)
        except DoctorProfile.DoesNotExist:
            return Response({'detail': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        qs = Appointment.objects.filter(doctor=doctor).select_related('patient__user')

        if start_date:
            qs = qs.filter(date_time__date__gte=start_date)
        if end_date:
            qs = qs.filter(date_time__date__lte=end_date)

        serializer = AppointmentSerializer(qs, many=True)
        return Response(serializer.data)
