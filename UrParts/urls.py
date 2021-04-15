"""UrParts URL Configuration"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.decorators import api_view

# Overriding default exception handlers for 404 & 403 errors.
from rest_framework.response import Response

handler404 = "UrParts.exception_handler.json_page_not_found"
handler403 = "UrParts.exception_handler.json_permission_denied"


@api_view(("GET",))
def health(request):
    return Response({"status": "healthy"})


schema_urls = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swaggerui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]


v1_urls = [
    path("", include("parts.v1.urls")),
]
urlpatterns = [
    # Admin URLs
    path("admin/", admin.site.urls),
    # Version 1 URLs
    path("api/", include([path("v1/", include(v1_urls))])),
    # Schema URLs
    *schema_urls,
    path("", health),
]
