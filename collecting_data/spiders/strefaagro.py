import scrapy
import uuid

class Title(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    origin = scrapy.Field()

class StrefaAgroSpider(scrapy.Spider):
    name = 'strefaagroSpider'
    start_urls = ['https://strefaagro.pl/wiadomosci']

    custom_settings = {
        'DEPTH_LIMIT': 1000,
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        for title in response.xpath("//div[contains(@class, 'atomsListingArticleTileWithSeparatedLink__info')]//h2[contains(@class, 'atomsTileTitle__title')]/text()"):
            title_content = title.get()[16:-13]
            yield Title(id=str(uuid.uuid4()), title=title_content, origin='strefaagro')

        for next_page in response.xpath("//li/a[contains(@class, 'atomsNavigationPagination__linkButton')]/@href").extract():
            next_page_url = 'https://strefaagro.pl' + next_page
            yield response.follow(next_page_url, self.parse)
