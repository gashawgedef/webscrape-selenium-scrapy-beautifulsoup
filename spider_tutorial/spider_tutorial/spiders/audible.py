import scrapy
from spider_tutorial.items import SpiderTutorialItem
from scrapy.loader import ItemLoader
import logging

class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["audible.com"]
    start_urls = ["https://www.audible.com/search"]

    def parse(self, response):
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

            item = loader.load_item()

            # Clean up the extracted strings
            if item.get('narrated_by') and "Narrated by:" in item['narrated_by']:
                item['narrated_by'] = item['narrated_by'].replace("Narrated by:", "").strip()
            if item.get('series') and "Series:" in item['series']:
                item['series'] = item['series'].replace("Series:", "").strip()
            if item.get('released_date') and "Release date:" in item['released_date']:
                item['released_date'] = item['released_date'].replace("Release date:", "").strip()
            if item.get('language') and "Language:" in item['language']:
                item['language'] = item['language'].replace("Language:", "").strip()
            if item.get('book_length') and "Length:" in item['book_length']:
                item['book_length'] = item['book_length'].replace("Length:", "").strip()

            logging.info(f"Scraped item: {item}")

            yield item

        next_page_url = response.css('span.nextButton a::attr(href)').get()
        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse)
