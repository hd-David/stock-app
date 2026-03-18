"""Telemedicine views."""
import logging
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.appointments.models import Appointment
from apps.users.permissions import IsDoctorOrAdmin
from .models import TelemedicineSession, ChatMessage
from .serializers import TelemedicineSessionSerializer, ChatMessageSerializer

logger = logging.getLogger(__name__)


class TelemedicineSessionCreateView(APIView):
    """Create a telemedicine session from an appointment."""
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]

    def post(self, request):
        appointment_id = request.data.get('appointment_id')
        if not appointment_id:
            return Response(
                {'detail': 'appointment_id is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'detail': 'Appointment not found.'}, status=status.HTTP_404_NOT_FOUND)

        if appointment.appointment_type != 'telemedicine':
            return Response(
                {'detail': 'This appointment is not a telemedicine appointment.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if hasattr(appointment, 'telemedicine_session'):
            return Response(
                TelemedicineSessionSerializer(appointment.telemedicine_session).data,
                status=status.HTTP_200_OK,
            )

        session = TelemedicineSession.objects.create(appointment=appointment)
        return Response(TelemedicineSessionSerializer(session).data, status=status.HTTP_201_CREATED)


class TelemedicineSessionDetailView(APIView):
    """Get session details."""
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            session = TelemedicineSession.objects.select_related(
                'appointment__patient__user', 'appointment__doctor__user'
            ).get(id=pk)
        except TelemedicineSession.DoesNotExist:
            return None

        if user.role == 'patient':
            if session.appointment.patient.user != user:
                return None
        elif user.role == 'doctor':
            if session.appointment.doctor.user != user:
                return None
        return session

    def get(self, request, pk):
        session = self.get_object(pk, request.user)
        if not session:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(TelemedicineSessionSerializer(session).data)


class JoinSessionView(APIView):
    """Join a telemedicine session."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            session = TelemedicineSession.objects.get(id=pk)
        except TelemedicineSession.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        now = timezone.now()

        if user.role == 'doctor' and session.appointment.doctor.user == user:
            if not session.doctor_joined_at:
                session.doctor_joined_at = now
        elif user.role == 'patient' and session.appointment.patient.user == user:
            if not session.patient_joined_at:
                session.patient_joined_at = now
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        if session.doctor_joined_at and session.patient_joined_at and not session.started_at:
            session.started_at = now
            session.status = 'active'

        session.save()
        return Response(TelemedicineSessionSerializer(session).data)


class EndSessionView(APIView):
    """End a telemedicine session (doctor or admin only)."""
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]

    def post(self, request, pk):
        try:
            session = TelemedicineSession.objects.get(id=pk)
        except TelemedicineSession.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 'doctor' and session.appointment.doctor.user != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        if session.status == 'ended':
            return Response({'detail': 'Session already ended.'}, status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        session.ended_at = now
        session.status = 'ended'

        if session.started_at:
            delta = now - session.started_at
            session.duration_minutes = int(delta.total_seconds() / 60)

        session.save()
        return Response(TelemedicineSessionSerializer(session).data)


class ChatMessageListCreateView(APIView):
    """List or create chat messages in a telemedicine session."""
    permission_classes = [IsAuthenticated]

    def get_session(self, pk, user):
        try:
            session = TelemedicineSession.objects.get(id=pk)
        except TelemedicineSession.DoesNotExist:
            return None
        if user.role == 'patient' and session.appointment.patient.user != user:
            return None
        if user.role == 'doctor' and session.appointment.doctor.user != user:
            return None
        return session

    def get(self, request, pk):
        session = self.get_session(pk, request.user)
        if not session:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        messages = ChatMessage.objects.filter(session=session)
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        session = self.get_session(pk, request.user)
        if not session:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(session=session, sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
