import uuid

from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from parts.constants import PART_MODEL_FIELDS
from parts.models import Part
from parts.serializers import PartSerializer
from UrParts.paginators import CustomPageNumberPagination


class PartListView(ListAPIView):
    serializer_class = PartSerializer
    pagination_class = CustomPageNumberPagination
    valid_query_params = ["page_size", "page", *PART_MODEL_FIELDS]

    def get_queryset(self):
        query_params = self._sanitise_params(self.request)
        return Part.objects.filter(**query_params)

    def _sanitise_params(self, request):
        params = request.GET.dict()
        for key in params.keys():
            if key not in self.valid_query_params:
                raise ValidationError("At lease one query param is invalid.")
        params.pop("page_size", None)
        params.pop("page", None)
        return params


class PartDetailView(APIView):
    def get(self, request, part_id, *args, **kwargs):
        part_id = self._validate_uuid(part_id)
        part = Part.objects.filter(id=part_id).first()
        if not part:
            raise NotFound(f"Part with uuid {part_id} not found.")
        return Response(PartSerializer(part).data)

    def _validate_uuid(self, uuid_str):
        """Check if the string is a valid uuid."""
        if isinstance(uuid_str, uuid.UUID):
            return uuid_str
        try:
            return uuid.UUID(uuid_str, version=4)
        except (TypeError, AttributeError, ValueError):
            raise ValidationError("Invalid part_id.")
