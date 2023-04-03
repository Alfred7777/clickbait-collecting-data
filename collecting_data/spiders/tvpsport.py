import scrapy
from scrapy_splash import SplashRequest
import uuid

class Title(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    origin = scrapy.Field()

class TVPSportSpider(scrapy.Spider):
    name = 'tvpsportSpider'
    start_urls = ['https://sport.tvp.pl/54053034/najnowsze']

    custom_settings = {
        'DEPTH_LIMIT': 1000,
        'DOWNLOAD_DELAY': 2,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse)   

    def parse(self, response):
        for title in response.xpath("//section[contains(@class, 'directory__content')]//div[contains(@class, 'col-lg-9')]/section[contains(@class, 'news-latest')]//a[contains(@class, 'news-latest__link')]/text()"):
            yield Title(id=str(uuid.uuid4()), title=title.get(), origin='tvpsport')

        for next_page in response.xpath("//section[contains(@class, 'pagination')]//a[contains(@class, 'pagination__next')]/@href").extract():
            yield SplashRequest(next_page, self.parse)
