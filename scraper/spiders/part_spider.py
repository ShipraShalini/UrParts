import scrapy


class PartSpider(scrapy.Spider):
    name = "part"
    start_urls = ["https://www.urparts.com/index.cfm/page/catalogue"]

    def _get_absolute_url(self, rel_url):
        return f"https://www.urparts.com/{rel_url}"

    def parse(self, response, **kwargs):
        for item in response.css("div.c_container li"):
            part = {"manufacturer": item.css("a::text").get().strip()}
            link = self._get_absolute_url(item.css("a::attr(href)").get())
            yield response.follow(
                link, callback=self.parse_categories, meta={"part": part}
            )

    def parse_categories(self, response):
        for item in response.css("div.c_container li"):
            part = response.meta["part"]
            part = {**part, "category": item.css("a::text").get().strip()}
            link = self._get_absolute_url(item.css("a::attr(href)").get())
            yield response.follow(link, callback=self.parse_models, meta={"part": part})

    def parse_models(self, response):
        for item in response.css("div.c_container li"):
            part = response.meta["part"]
            part["model"] = item.css("a::text").get().strip()
            link = self._get_absolute_url(item.css("a::attr(href)").get())
            yield response.follow(link, callback=self.parse_parts, meta={"part": part})

    def parse_modelsections(self, response):
        # ToDo check why this is not working.
        for item in response.css("div.modelSection li"):
            part = response.meta["part"]
            link = self._get_absolute_url(item.css("a::attr(href)").get())
            yield response.follow(link, callback=self.parse_parts, meta={"part": part})
        part = response.meta["part"]
        yield response.follow(
            response.url, callback=self.parse_parts, meta={"part": part}
        )

    def parse_parts(self, response):
        for item in response.css("div.c_container li"):
            part = response.meta["part"]
            part["part"] = item.css("a::text").get().strip().replace(" -", "")
            part["part_category"] = item.css("span::text").get()
            yield part
