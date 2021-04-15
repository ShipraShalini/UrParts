"""UrParts URL Configuration"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.decorators import api_view


@api_view(("GET",))
def health(request):
    return JsonResponse({"status": "healthy"})


schema_urls = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swaggerui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


v1_urls = [
    # path("", include("parts.v1.urls")),
]
urlpatterns = [
    # Admin URLs
    path("admin/", admin.site.urls),
    # Verion 1 URLs
    path(
        "api/",
        include(
            [
                path("v1/", include(v1_urls)),
            ]
        ),
    ),
    # Schema URLs
    *schema_urls,
    path("", health),
]
