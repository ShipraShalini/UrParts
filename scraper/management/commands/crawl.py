# Reference: https://blog.theodo.com/2019/01/data-scraping-scrapy-django-integration/
from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.part_spider import PartSpider


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())

        process.crawl(PartSpider)
        process.start()
