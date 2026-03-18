"""Patient views."""
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsPatient, IsDoctorOrAdmin
from .models import PatientProfile
from .serializers import PatientProfileSerializer


class PatientProfileView(APIView):
    """Get or update the authenticated patient's profile."""
    permission_classes = [IsAuthenticated, IsPatient]

    def get_object(self):
        profile, _ = PatientProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get(self, request):
        profile = self.get_object()
        serializer = PatientProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = self.get_object()
        serializer = PatientProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile = self.get_object()
        serializer = PatientProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientListView(generics.ListAPIView):
    """List all patients (admin/doctor only)."""
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]
    queryset = PatientProfile.objects.select_related('user').all()
    filterset_fields = ['blood_type']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['created_at', 'user__last_name']


class PatientDetailView(generics.RetrieveAPIView):
    """Retrieve a specific patient's profile (admin/doctor only)."""
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]
    queryset = PatientProfile.objects.select_related('user').all()
