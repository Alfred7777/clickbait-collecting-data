import scrapy
from scrapy_splash import SplashRequest
import uuid

class Title(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    origin = scrapy.Field()

class NaukaWPolsceSpider(scrapy.Spider):
    name = 'naukawpolsceSpider'
    start_urls = ['https://naukawpolsce.pl/news']

    custom_settings = {
        'DEPTH_LIMIT': 1000,
        'DOWNLOAD_DELAY': 2,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse)   

    def parse(self, response):
        for title in response.xpath("//li/a/h2[contains(@class, 'title')]/text()"):
            yield Title(id=str(uuid.uuid4()), title=title.get(), origin='naukawpolsce')

        for next_page in response.xpath("//li[contains(@class, 'pager__item--next')]/a/@href").extract():
            next_page_url = "https://naukawpolsce.pl/news" + next_page
            yield SplashRequest(next_page_url, self.parse)
            