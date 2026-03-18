"""EMR views."""
import logging
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patients.models import PatientProfile
from apps.doctors.models import DoctorProfile
from apps.users.permissions import IsDoctor, IsDoctorOrAdmin
from .models import MedicalRecord, Prescription, LabResult, MedicalDocument
from .serializers import (
    MedicalRecordSerializer,
    MedicalRecordCreateSerializer,
    PrescriptionSerializer,
    LabResultSerializer,
    MedicalDocumentSerializer,
)

logger = logging.getLogger(__name__)


class MedicalRecordListCreateView(APIView):
    """List medical records (filtered by role) or create a new record (doctors only)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == 'patient':
            try:
                patient = PatientProfile.objects.get(user=user)
                qs = MedicalRecord.objects.filter(patient=patient).select_related(
                    'doctor__user', 'patient__user'
                ).prefetch_related('prescriptions', 'lab_results', 'documents')
            except PatientProfile.DoesNotExist:
                qs = MedicalRecord.objects.none()
        elif user.role == 'doctor':
            try:
                doctor = DoctorProfile.objects.get(user=user)
                qs = MedicalRecord.objects.filter(doctor=doctor).select_related(
                    'doctor__user', 'patient__user'
                ).prefetch_related('prescriptions', 'lab_results', 'documents')
            except DoctorProfile.DoesNotExist:
                qs = MedicalRecord.objects.none()
        else:
            qs = MedicalRecord.objects.select_related(
                'doctor__user', 'patient__user'
            ).prefetch_related('prescriptions', 'lab_results', 'documents').all()

        serializer = MedicalRecordSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role not in ['doctor', 'admin']:
            return Response(
                {'detail': 'Only doctors or admins can create medical records.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            doctor = DoctorProfile.objects.get(user=request.user)
        except DoctorProfile.DoesNotExist:
            return Response(
                {'detail': 'Doctor profile not found.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = MedicalRecordCreateSerializer(data=request.data)
        if serializer.is_valid():
            record = serializer.save(doctor=doctor)
            return Response(MedicalRecordSerializer(record).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicalRecordDetailView(APIView):
    """Retrieve, update, or delete a medical record."""
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            record = MedicalRecord.objects.select_related(
                'doctor__user', 'patient__user'
            ).prefetch_related('prescriptions', 'lab_results', 'documents').get(id=pk)
        except MedicalRecord.DoesNotExist:
            return None

        if user.role == 'patient':
            if not hasattr(user, 'patient_profile') or record.patient.user != user:
                return None
        elif user.role == 'doctor':
            if not hasattr(user, 'doctor_profile') or record.doctor.user != user:
                return None
        return record

    def get(self, request, pk):
        record = self.get_object(pk, request.user)
        if not record:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(MedicalRecordSerializer(record).data)

    def patch(self, request, pk):
        if request.user.role not in ['doctor', 'admin']:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        record = self.get_object(pk, request.user)
        if not record:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MedicalRecordCreateSerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(MedicalRecordSerializer(record).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrescriptionListCreateView(generics.ListCreateAPIView):
    """List or create prescriptions for a medical record."""
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]

    def get_queryset(self):
        record_id = self.kwargs.get('record_id')
        return Prescription.objects.filter(record__id=record_id)

    def perform_create(self, serializer):
        record_id = self.kwargs.get('record_id')
        record = MedicalRecord.objects.get(id=record_id)
        serializer.save(record=record)


class LabResultListCreateView(generics.ListCreateAPIView):
    """List or create lab results for a medical record."""
    serializer_class = LabResultSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]

    def get_queryset(self):
        record_id = self.kwargs.get('record_id')
        return LabResult.objects.filter(record__id=record_id)

    def perform_create(self, serializer):
        record_id = self.kwargs.get('record_id')
        record = MedicalRecord.objects.get(id=record_id)
        serializer.save(record=record)


class MedicalDocumentListCreateView(generics.ListCreateAPIView):
    """List or upload documents for a medical record."""
    serializer_class = MedicalDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        record_id = self.kwargs.get('record_id')
        return MedicalDocument.objects.filter(record__id=record_id)

    def perform_create(self, serializer):
        record_id = self.kwargs.get('record_id')
        record = MedicalRecord.objects.get(id=record_id)
        serializer.save(record=record, uploaded_by=self.request.user)
