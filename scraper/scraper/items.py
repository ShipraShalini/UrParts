import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags

def strip_text(text):
    return text.strip()

class PartItem(scrapy.Item):
    manufacturer = scrapy.Field()
    category = scrapy.Field()
    model = scrapy.Field()
    part = scrapy.Field()
    part_category = scrapy.Field()
