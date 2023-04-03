import scrapy
import uuid

class Title(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    origin = scrapy.Field()

class PudelekSpider(scrapy.Spider):
    name = 'pudelekSpider'
    start_urls = ['https://www.pudelek.pl/archiwum/']

    custom_settings = {
        'DEPTH_LIMIT': 1000,
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        for title in response.xpath("//ul[contains(@class, 'v8y7lv-2')]/li//a[contains(@class, 'hfzlbj-0')]/text()"):
            yield Title(id=str(uuid.uuid4()), title=title.get(), origin='pudelek')

        for next_page in response.xpath("//div[contains(@class, 'jkvqje-0')]/div[contains(@class, 'sc-1kpe1m2-0')]/a"):
            yield response.follow(next_page, self.parse)
