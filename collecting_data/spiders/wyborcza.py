import scrapy
import uuid

class Title(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    origin = scrapy.Field()

class WyborczaSpider(scrapy.Spider):
    name = 'wyborczaSpider'
    start_urls = ['https://wyborcza.pl/0,75248.html?str=1_23719317']

    custom_settings = {
        'DEPTH_LIMIT': 1000,
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        for title in response.xpath("//div[contains(@class, 'column-22')]//li/h3/a/text()"):
            yield Title(id=str(uuid.uuid4()), title=title.get(), origin='wyborcza')

        for next_page in response.xpath("//div[contains(@class, 'pages')]/a[contains(@class, 'next')]"):
            yield response.follow(next_page, self.parse)
