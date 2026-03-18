"""Patient URL patterns."""
from django.urls import path
from .views import PatientProfileView, PatientListView, PatientDetailView

urlpatterns = [
    path('profile/', PatientProfileView.as_view(), name='patient-profile'),
    path('', PatientListView.as_view(), name='patient-list'),
    path('<uuid:pk>/', PatientDetailView.as_view(), name='patient-detail'),
]
