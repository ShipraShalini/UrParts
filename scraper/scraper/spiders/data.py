import scrapy

from scraper.items import PartItem

class PartSpider(scrapy.Spider):
    name = 'part'
    start_urls = ["https://www.urparts.com/index.cfm/page/catalogue"]

    def _get_absolute_url(self, rel_url):
        return f'https://www.urparts.com/{rel_url}'

    def parse(self, response, **kwargs):
        part = PartItem()
        for item in response.css('div.c_container li'):
            part['manufacturer'] = item.css('a::text').get().strip()
            if part['manufacturer'] != 'Ammann':
                continue
            link = self._get_absolute_url(item.css('a::attr(href)').get())
            yield response.follow(
                link,
                callback=self.parse_categories,
                meta={'part': part}
            )

    def parse_categories(self, response):
        for item in response.css('div.c_container li'):
            part = response.meta['part']
            part['category'] = item.css('a::text').get().strip()

            link = self._get_absolute_url(item.css('a::attr(href)').get())
            yield response.follow(
                link,
                callback=self.parse_models,
                meta={'part': part}
            )

    def parse_models(self, response):
        part = response.meta['part']
        for item in response.css('div.c_container li'):
            part['model'] = item.css('a::text').get().strip()

            link = self._get_absolute_url(item.css('a::attr(href)').get())
            yield response.follow(
                link,
                callback=self.parse_modelsections,
                meta={'part': part}
            )

    def parse_modelsections(self, response):
        for item in response.css('div.c_container.modelSection li'):
            part = response.meta['part']
            link = self._get_absolute_url(item.css('a::attr(href)').get())
            yield response.follow(
                link,
                callback=self.parse_parts,
                meta={'part': part}
            )
        part = response.meta['part']
        return response.follow(
            response.url,
            callback=self.parse_parts,
            meta={'part': part}
        )

    def parse_parts(self, response):
        for item in response.css('div.c_container li'):
            part = response.meta['part']
            part['part'], part['part_category'] = self._sanitise_parts(item.css('a::text'))
            print(part)
            yield part

    def _sanitise_parts(self, extracted_name):
        part, _, part_category = extracted_name.strip().rpartition(' - ')
        return part, part_category