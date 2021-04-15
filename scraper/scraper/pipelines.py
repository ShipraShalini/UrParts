# Define your item pipelines here


class ScraperPipeline:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        if len(self.items) >= 1000:
            self.insert_current_items()
        return item

    def insert_current_items(self):
        items = self.items
        self.items = []
        self.insert_to_database(items)

    def close_spider(self, spider):
        self.insert_current_items()
