"""Doctor views."""
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsDoctor, IsDoctorOrAdmin
from .models import DoctorProfile, DoctorAvailability
from .serializers import DoctorProfileSerializer, DoctorProfileCreateSerializer, DoctorAvailabilitySerializer


class DoctorProfileView(APIView):
    """Get or update the authenticated doctor's profile."""
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_object(self):
        profile, _ = DoctorProfile.objects.get_or_create(
            user=self.request.user,
            defaults={'license_number': f'PENDING-{self.request.user.id}'},
        )
        return profile

    def get(self, request):
        profile = self.get_object()
        serializer = DoctorProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = self.get_object()
        serializer = DoctorProfileCreateSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(DoctorProfileSerializer(profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile = self.get_object()
        serializer = DoctorProfileCreateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(DoctorProfileSerializer(profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorListView(generics.ListAPIView):
    """List all doctors. Open to authenticated users."""
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = DoctorProfile.objects.select_related('user').prefetch_related('availability').all()
    filterset_fields = ['specialization', 'is_accepting_patients']
    search_fields = ['user__first_name', 'user__last_name', 'specialization', 'languages_spoken']
    ordering_fields = ['years_of_experience', 'consultation_fee', 'created_at']


class DoctorDetailView(generics.RetrieveAPIView):
    """Retrieve a specific doctor's profile."""
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = DoctorProfile.objects.select_related('user').prefetch_related('availability').all()


class DoctorAvailabilityView(APIView):
    """Manage doctor availability schedule."""
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request):
        profile = DoctorProfile.objects.get(user=request.user)
        availability = DoctorAvailability.objects.filter(doctor=profile)
        serializer = DoctorAvailabilitySerializer(availability, many=True)
        return Response(serializer.data)

    def post(self, request):
        profile = DoctorProfile.objects.get(user=request.user)
        serializer = DoctorAvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(doctor=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorAvailabilityDetailView(APIView):
    """Update or delete a specific availability slot."""
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_object(self, pk, user):
        try:
            profile = DoctorProfile.objects.get(user=user)
            return DoctorAvailability.objects.get(id=pk, doctor=profile)
        except (DoctorProfile.DoesNotExist, DoctorAvailability.DoesNotExist):
            return None

    def put(self, request, pk):
        slot = self.get_object(pk, request.user)
        if not slot:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DoctorAvailabilitySerializer(slot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        slot = self.get_object(pk, request.user)
        if not slot:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DoctorAvailabilitySerializer(slot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        slot = self.get_object(pk, request.user)
        if not slot:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        slot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
