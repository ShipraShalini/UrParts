# Define your item pipelines here
from datetime import datetime

from parts.models import Part


class ScraperPipeline:
    BATCH_SIZE = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []

    def process_item(self, item, spider):
        part = Part(**item, created_at=datetime.utcnow())
        self.items.append(part)
        if len(self.items) == self.BATCH_SIZE:
            self.bulk_insert()
        return item

    def close_spider(self, spider):
        self.bulk_insert()

    def bulk_insert(self):
        Part.objects.bulk_create(self.items, ignore_conflicts=True)
        self.items = []
