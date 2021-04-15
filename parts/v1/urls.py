from django.urls import path

from parts.v1.views import PartDetailView, PartListView

app_name = "parts"


urlpatterns = [
    path("parts/", PartListView.as_view(), name="part-list"),
    path("parts/<uuid:part_id>", PartDetailView.as_view(), name="part-detail"),
]
