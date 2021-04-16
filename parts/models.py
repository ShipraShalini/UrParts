import uuid

from django.db import models
from django.db.models import DateTimeField, UUIDField


class Part(models.Model):
    uuid = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manufacturer = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    part = models.CharField(max_length=100)
    part_category = models.CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["manufacturer", "category", "model", "part", "part_category"],
                name="unique_part_entry",
            )
        ]

    def __str__(self):
        """Return Return string representation of the model."""
        return f"{self.manufacturer} | {self.model} | {self.part}"
