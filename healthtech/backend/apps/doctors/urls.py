"""Doctor URL patterns."""
from django.urls import path
from .views import (
    DoctorProfileView,
    DoctorListView,
    DoctorDetailView,
    DoctorAvailabilityView,
    DoctorAvailabilityDetailView,
)

urlpatterns = [
    path('profile/', DoctorProfileView.as_view(), name='doctor-profile'),
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('<uuid:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('availability/', DoctorAvailabilityView.as_view(), name='doctor-availability'),
    path('availability/<uuid:pk>/', DoctorAvailabilityDetailView.as_view(), name='doctor-availability-detail'),
]
