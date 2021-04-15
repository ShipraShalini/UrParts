from datetime import datetime
from urllib.parse import quote

from django.views.defaults import page_not_found, permission_denied
from rest_framework import status
from rest_framework.response import Response

from UrParts.constants import BUILTIN_ERROR_MESSAGE, CLIENT_ERROR_SET
from UrParts.utils import is_api_request


def get_exception_message(exception):
    """Get error message from the exception."""
    exception_name = exception.__class__.__name__
    message = BUILTIN_ERROR_MESSAGE.get(exception_name)
    if message:
        return message
    message = getattr(exception, "message", None)
    if message is not None:
        return str(message)
    message = getattr(exception, "args", None)
    if message:
        return str(message[0] if isinstance(message, tuple) else message)
    else:
        return exception_name


class ExceptionHandler:
    """Exception handler for the API requests."""

    def get_ip(self, headers):
        """Get IP from the request headers."""
        return headers.get("HTTP_X_FORWARDED_FOR") or headers.get("REMOTE_ADDR")

    def get_status_code(self, exc):
        """Get HTTP status code for the exception."""
        status_code = getattr(exc, "status_code", None)
        if status_code is not None:
            return status_code
        if exc.__class__.__name__ in CLIENT_ERROR_SET:
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def handle_exception(self, request, exception):
        headers = request.headers
        status_code = self.get_status_code(exception)
        error_data = {
            "status": status_code,
            "date": datetime.utcnow(),
            "IP": self.get_ip(headers),
            "user": getattr(request.user, "username", "AnonymousUser"),
            "error": exception.__class__.__name__,
            "error_msg": get_exception_message(exception),
        }
        return error_data


def drf_exception_handler(exception, context):
    """Custom exception handler for DRF."""
    request = context["request"]
    error_data = ExceptionHandler().handle_exception(request, exception)
    return Response(error_data, status=error_data["status"])


def json_page_not_found(request, exception, *args, **kwargs):
    """Override 404 error to return a JSON Error"""
    if not is_api_request(request):
        return page_not_found(request, exception, *args, **kwargs)
    context = {
        "request_path": quote(request.path),
        "exception": get_exception_message(exception),
    }
    return Response(context, status=status.HTTP_404_NOT_FOUND)


def json_permission_denied(request, exception, *args, **kwargs):
    """Override 403 error to return a JSON Error"""
    if not is_api_request(request):
        return permission_denied(request, exception, *args, **kwargs)
    context = {
        "request_path": quote(request.path),
        "exception": get_exception_message(exception),
    }
    return Response(context, status=status.HTTP_403_FORBIDDEN)
