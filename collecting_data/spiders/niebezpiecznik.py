import scrapy
from scrapy_splash import SplashRequest
import uuid

class Title(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    origin = scrapy.Field()

class NiebezpiecznikSpider(scrapy.Spider):
    name = 'niebezpiecznikSpider'
    start_urls = ['https://niebezpiecznik.pl/page/13']

    custom_settings = {
        'DEPTH_LIMIT': 1000,
        'DOWNLOAD_DELAY': 2,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse)   

    def parse(self, response):
        for title in response.xpath("//div[contains(@class, 'post')]//h2/a/text()"):
            yield Title(id=str(uuid.uuid4()), title=title.get(), origin='niebezpiecznik')

        for next_page in response.xpath("//div[contains(@class, 'navigation')]/div[contains(@class, 'left')]//a/@href").extract():
            yield SplashRequest(next_page, self.parse)
            