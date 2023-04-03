import scrapy
import uuid

class Title(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    origin = scrapy.Field()

class WikiNewsSpider(scrapy.Spider):
    name = 'wikinewsSpider'
    start_urls = ['https://pl.wikinews.org/wiki/Portal:Maj_2022']

    custom_settings = {
        'DEPTH_LIMIT': 1000,
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        for title in response.xpath("//div[contains(@class, 'mw-parser-output')]/ul/li/a/text()"):
            yield Title(id=str(uuid.uuid4()), title=title.get(), origin='wikinews')

        for next_page in response.xpath("//div[contains(@class, 'mw-parser-output')]/center[1]/a[1]"):
            yield response.follow(next_page, self.parse)
