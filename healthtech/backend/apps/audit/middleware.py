"""Audit logging middleware."""
import logging
from django.utils.deprecation import MiddlewareMixin
from apps.audit.models import AuditLog

logger = logging.getLogger(__name__)


class AuditLogMiddleware(MiddlewareMixin):
    """Middleware to automatically log API requests."""

    EXCLUDED_PATHS = ['/health/', '/static/', '/media/', '/swagger/', '/redoc/']

    def process_response(self, request, response):
        """Log the request after response is generated."""
        if any(request.path.startswith(p) for p in self.EXCLUDED_PATHS):
            return response

        if not request.path.startswith('/api/'):
            return response

        try:
            user = request.user if request.user.is_authenticated else None

            action_map = {
                'GET': 'READ',
                'POST': 'CREATE',
                'PUT': 'UPDATE',
                'PATCH': 'UPDATE',
                'DELETE': 'DELETE',
            }
            action = action_map.get(request.method, 'READ')

            path_parts = request.path.strip('/').split('/')
            resource = path_parts[2] if len(path_parts) > 2 else 'unknown'
            resource_id = path_parts[3] if len(path_parts) > 3 else ''

            ip_address = self._get_client_ip(request)

            AuditLog.objects.create(
                user=user,
                action=action,
                resource=resource,
                resource_id=resource_id,
                ip_address=ip_address or None,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                request_method=request.method,
                request_path=request.path,
                response_status=response.status_code,
            )
        except Exception as e:
            logger.error(f"Failed to create audit log: {e}")

        return response

    def _get_client_ip(self, request) -> str:
        """Extract client IP from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')
