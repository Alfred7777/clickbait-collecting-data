import scrapy
from scrapy_splash import SplashRequest
import uuid

class Title(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    origin = scrapy.Field()

class Space24Spider(scrapy.Spider):
    name = 'space24Spider'
    start_urls = ['https://space24.pl/wiadomosci']

    custom_settings = {
        'DEPTH_LIMIT': 1000,
        'DOWNLOAD_DELAY': 2,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse)   

    def parse(self, response):
        for title in response.xpath("//li[contains(@class, 'thumbnails-list__item')]//a/div/text()"):
            title_content = title.get()[17:-15]
            yield Title(id=str(uuid.uuid4()), title=title_content, origin='space24')

        for next_page in response.xpath("//ul[contains(@class, 'pagination')]//li[contains(@class, 'page-item')]//a[contains(@aria-label, 'Następna strona')]/@href").extract():
            next_page_url = "https://space24.pl/" + next_page
            yield SplashRequest(next_page_url, self.parse)
            