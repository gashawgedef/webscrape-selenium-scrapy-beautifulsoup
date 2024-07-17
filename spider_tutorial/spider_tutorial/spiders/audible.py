import scrapy
from spider_tutorial.items import SpiderTutorialItem
from scrapy.loader import ItemLoader

class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["audible.com"]
    start_urls = ["https://www.audible.com/search"]

    def parse(self, response):
        # Select the product container using the correct CSS selector
        product_container = response.css('div.adbl-impression-container > div > span > ul > li.bc-list-item')

        for product in product_container:
            loader = ItemLoader(item=SpiderTutorialItem(), selector=product)
            loader.add_css('book_title', 'h3.bc-heading > a::text')
            loader.add_css('book_author', 'li.authorLabel > span > a::text')
            loader.add_css('narrated_by', 'li.narratorLabel > span > a::text')
            loader.add_css('series', 'li.seriesLabel > span > a::text')
            loader.add_css('book_length', 'li.runtimeLabel > span::text')
            loader.add_css('released_date', 'li.releaseDateLabel > span::text')
            loader.add_css('ratings', 'li.ratingsLabel > span::text')
            loader.add_css('language', 'li.languageLabel > span::text')

            yield loader.load_item()

        # Handle pagination
        next_page_url = response.css('span.nextButton a::attr(href)').get()
        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse)
