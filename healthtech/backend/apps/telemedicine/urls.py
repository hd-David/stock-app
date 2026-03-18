"""Telemedicine URL patterns."""
from django.urls import path
from .views import (
    TelemedicineSessionCreateView,
    TelemedicineSessionDetailView,
    JoinSessionView,
    EndSessionView,
    ChatMessageListCreateView,
)

urlpatterns = [
    path('sessions/', TelemedicineSessionCreateView.as_view(), name='telemedicine-session-create'),
    path('sessions/<uuid:pk>/', TelemedicineSessionDetailView.as_view(), name='telemedicine-session-detail'),
    path('sessions/<uuid:pk>/join/', JoinSessionView.as_view(), name='telemedicine-session-join'),
    path('sessions/<uuid:pk>/end/', EndSessionView.as_view(), name='telemedicine-session-end'),
    path('sessions/<uuid:pk>/messages/', ChatMessageListCreateView.as_view(), name='telemedicine-chat-messages'),
]
