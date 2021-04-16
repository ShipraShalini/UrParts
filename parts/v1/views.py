from typing import Dict

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView

from parts.constants import PART_MODEL_FIELDS
from parts.models import Part
from parts.serializers import PartSerializer
from UrParts.paginators import CustomPageNumberPagination


class PartListView(ListAPIView):
    """Return a list of Parts."""

    serializer_class = PartSerializer
    pagination_class = CustomPageNumberPagination
    valid_query_params = ["page_size", "page", *PART_MODEL_FIELDS]

    def get_queryset(self):
        """Returns queryset filtered based on the query params."""
        query_params = self._sanitise_params(self.request.GET.dict())
        return Part.objects.filter(**query_params)

    def _sanitise_params(self, params: Dict):
        """Check if the params are valid. Removes pagination params."""
        for key in params.keys():
            if key not in self.valid_query_params:
                raise ValidationError("At lease one query param is invalid.")
        params.pop("page_size", None)
        params.pop("page", None)
        return params


@extend_schema_view(
    retrieve=extend_schema(description="Testing the description extend_schema_view")
)
class PartDetailView(RetrieveAPIView):
    lookup_field = "uuid"
    lookup_url_kwarg = "part_id"
    serializer_class = PartSerializer
