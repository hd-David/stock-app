"""Triage views."""
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patients.models import PatientProfile
from apps.users.permissions import IsPatient, IsDoctorOrAdmin
from .models import SymptomCheck
from .serializers import SymptomCheckSerializer, SymptomCheckCreateSerializer
from .triage_engine import SYMPTOM_CONDITIONS


class SymptomCheckCreateView(APIView):
    """Run a triage symptom check."""
    permission_classes = [IsAuthenticated, IsPatient]

    def post(self, request):
        try:
            patient = PatientProfile.objects.get(user=request.user)
        except PatientProfile.DoesNotExist:
            return Response(
                {'detail': 'Patient profile not found. Please complete your profile first.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SymptomCheckCreateSerializer(data=request.data)
        if serializer.is_valid():
            check = serializer.save(patient=patient)
            return Response(SymptomCheckSerializer(check).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SymptomCheckListView(generics.ListAPIView):
    """List a patient's symptom check history."""
    serializer_class = SymptomCheckSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            try:
                patient = PatientProfile.objects.get(user=user)
                return SymptomCheck.objects.filter(patient=patient)
            except PatientProfile.DoesNotExist:
                return SymptomCheck.objects.none()
        # Doctors and admins can list all
        return SymptomCheck.objects.select_related('patient__user').all()


class SymptomCheckDetailView(generics.RetrieveAPIView):
    """Retrieve a specific symptom check."""
    serializer_class = SymptomCheckSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            try:
                patient = PatientProfile.objects.get(user=user)
                return SymptomCheck.objects.filter(patient=patient)
            except PatientProfile.DoesNotExist:
                return SymptomCheck.objects.none()
        return SymptomCheck.objects.select_related('patient__user').all()


class AvailableSymptomsView(APIView):
    """Return the list of all recognized symptoms."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        symptoms = sorted(SYMPTOM_CONDITIONS.keys())
        return Response({'symptoms': symptoms, 'count': len(symptoms)})
