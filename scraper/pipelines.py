from django.db import IntegrityError

from parts.models import Part


class ScraperPipeline:
    def process_item(self, item, spider):
        """Save part to the db."""
        try:
            Part.objects.create(**item)
        except IntegrityError:
            pass
        return item
