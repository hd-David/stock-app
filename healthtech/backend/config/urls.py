from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="HealthTech API",
        default_version='v1',
        description="HealthTech Platform API Documentation",
        terms_of_service="https://www.healthtech.com/terms/",
        contact=openapi.Contact(email="api@healthtech.com"),
        license=openapi.License(name="Proprietary"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/patients/', include('apps.patients.urls')),
    path('api/v1/doctors/', include('apps.doctors.urls')),
    path('api/v1/appointments/', include('apps.appointments.urls')),
    path('api/v1/emr/', include('apps.emr.urls')),
    path('api/v1/telemedicine/', include('apps.telemedicine.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/audit/', include('apps.audit.urls')),
    path('api/v1/triage/', include('apps.triage.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
