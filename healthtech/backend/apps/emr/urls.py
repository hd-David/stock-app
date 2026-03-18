"""EMR URL patterns."""
from django.urls import path
from .views import (
    MedicalRecordListCreateView,
    MedicalRecordDetailView,
    PrescriptionListCreateView,
    LabResultListCreateView,
    MedicalDocumentListCreateView,
)

urlpatterns = [
    path('records/', MedicalRecordListCreateView.as_view(), name='medical-record-list-create'),
    path('records/<uuid:pk>/', MedicalRecordDetailView.as_view(), name='medical-record-detail'),
    path('records/<uuid:record_id>/prescriptions/', PrescriptionListCreateView.as_view(), name='prescription-list-create'),
    path('records/<uuid:record_id>/lab-results/', LabResultListCreateView.as_view(), name='lab-result-list-create'),
    path('records/<uuid:record_id>/documents/', MedicalDocumentListCreateView.as_view(), name='medical-document-list-create'),
]
