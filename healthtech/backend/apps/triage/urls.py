"""Triage URL patterns."""
from django.urls import path
from .views import (
    SymptomCheckCreateView,
    SymptomCheckListView,
    SymptomCheckDetailView,
    AvailableSymptomsView,
)

urlpatterns = [
    path('check/', SymptomCheckCreateView.as_view(), name='symptom-check-create'),
    path('history/', SymptomCheckListView.as_view(), name='symptom-check-list'),
    path('history/<uuid:pk>/', SymptomCheckDetailView.as_view(), name='symptom-check-detail'),
    path('symptoms/', AvailableSymptomsView.as_view(), name='available-symptoms'),
]
