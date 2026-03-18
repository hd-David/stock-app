"""Appointment URL patterns."""
from django.urls import path
from .views import (
    AppointmentListCreateView,
    AppointmentDetailView,
    AppointmentCancelView,
    AppointmentCompleteView,
    DoctorCalendarView,
)

urlpatterns = [
    path('', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('<uuid:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('<uuid:pk>/cancel/', AppointmentCancelView.as_view(), name='appointment-cancel'),
    path('<uuid:pk>/complete/', AppointmentCompleteView.as_view(), name='appointment-complete'),
    path('calendar/<uuid:pk>/', DoctorCalendarView.as_view(), name='doctor-calendar'),
]
