import scrapy


class PartSpider(scrapy.Spider):
    """Scraper for getting data from https://www.urparts.com website."""

    name = "part"
    start_urls = ["https://www.urparts.com/index.cfm/page/catalogue"]

    def _get_absolute_url(self, rel_url: str):
        return f"https://www.urparts.com/{rel_url}"

    def parse(self, response, **kwargs):
        """Get all the manufacturers."""
        for item in response.css("div.c_container li"):
            part = {"manufacturer": item.css("a::text").get().strip()}
            link = self._get_absolute_url(item.css("a::attr(href)").get())
            yield response.follow(
                link, callback=self.parse_categories, meta={"part": part}
            )

    def parse_categories(self, response):
        """Get categories for all manufacturers."""
        for item in response.css("div.c_container li"):
            part = response.meta["part"]
            part = {**part, "category": item.css("a::text").get().strip()}
            link = self._get_absolute_url(item.css("a::attr(href)").get())
            yield response.follow(link, callback=self.parse_models, meta={"part": part})

    def parse_models(self, response):
        """Get models for all categories."""
        for item in response.css("div.c_container li"):
            part = response.meta["part"]
            part["model"] = item.css("a::text").get().strip()
            link = self._get_absolute_url(item.css("a::attr(href)").get())
            yield response.follow(link, callback=self.parse_parts, meta={"part": part})

    def parse_modelsections(self, response):
        """Get sections for models, if present else move to parts."""
        # ToDo: check why this is not working.
        for item in response.css("ul.finalmenu li"):
            part = response.meta["part"]
            link = self._get_absolute_url(item.css("a::attr(href)").get())
            yield response.follow(link, callback=self.parse_parts, meta={"part": part})
        part = response.meta["part"]
        yield response.follow(
            response.url, callback=self.parse_parts, meta={"part": part}
        )

    def parse_parts(self, response):
        """Get parts for models/sections."""
        for item in response.css("div.c_container.allparts li"):
            part = response.meta["part"]
            part["part"] = item.css("a::text").get().strip().replace(" -", "")
            part["part_category"] = item.css("span::text").get()
            yield part
