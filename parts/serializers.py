from rest_framework.serializers import ModelSerializer

from parts.models import Part


class PartSerializer(ModelSerializer):
    class Meta:
        model = Part
        fields = "__all__"
