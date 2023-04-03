from scipy.fft import next_fast_len
import scrapy
from scrapy_splash import SplashRequest
import uuid

class Title(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    origin = scrapy.Field()

class TabletowoSpider(scrapy.Spider):
    name = 'tabletowoSpider'
    start_urls = ['https://www.tabletowo.pl/page/2/']

    custom_settings = {
        'DEPTH_LIMIT': 1000,
        'DOWNLOAD_DELAY': 2,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse)   

    def parse(self, response):
        for title in response.xpath("//h3[contains(@class, 'title')]/a/text()"):
            yield Title(id=str(uuid.uuid4()), title=title.get(), origin='tabletowo')

        for next_page in response.xpath("//a[contains(@class, 'next page-numbers')]/@href").extract():
            yield SplashRequest(next_page, self.parse)
            