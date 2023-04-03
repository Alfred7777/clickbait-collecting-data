import scrapy
import uuid

class Title(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    origin = scrapy.Field()

class WPwiadomosciSpider(scrapy.Spider):
    name = 'wpwiadomosciSpider'
    start_urls = ['https://wiadomosci.wp.pl/2']

    custom_settings = {
        'DEPTH_LIMIT': 1000,
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        for title in response.xpath("//div[contains(@class, 'a2B3ie5k')]//div[contains(@class, 'a2eMLotm')]//a[contains(@class, 'a2PrHTUx')]//h2[contains(@class, 'aP9eOAhb')]/text()"):
            yield Title(id=str(uuid.uuid4()), title=title.get(), origin='wpwiadomosci')

        for next_page in response.xpath("//ul[contains(@class, 'aKxRAdgW')]/li[contains(@class, 'an74oXHA')][last()]/a"):
            yield response.follow(next_page, self.parse)
