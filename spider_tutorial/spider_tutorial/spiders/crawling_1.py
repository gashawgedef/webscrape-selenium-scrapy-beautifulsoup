from typing import Iterable
import scrapy


class Crawling1Spider(scrapy.Spider):
    name = "crawling_1"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]
    def start_requests(self):
        yield scrapy.Request(url="https://www.audible.com/search",callback=self.parse,
                       headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'})

    def parse(self, response):
        # Select the product container using the correct CSS selector
        product_container = response.css('div.adbl-impression-container > div > span > ul > li.bc-list-item')
        
        for product in product_container:
            # Extract the details from each product (li element)
            book_author = product.css('li.authorLabel > span > a::text').getall()
            book_length = product.css('li.runtimeLabel > span::text').get()
            book_title = product.css('h3.bc-heading > a::text').get()
            narrated_by = product.css('li.narratorLabel > span > a::text').get()
            series = product.css('li.seriesLabel > span > a::text').get()
            released_date = product.css('li.releaseDateLabel > span::text').get()
            ratings = product.css('li.ratingsLabel > span::text').get()
            language = product.css('li.languageLabel > span::text').get()
            
            # Clean up the extracted strings
            if book_author:
                book_author = [author.strip() for author in book_author]
            if narrated_by and "Narrated by:" in narrated_by:
                narrated_by = narrated_by.replace("Narrated by:", "").strip()
            if series and "Series:" in series:
                series = series.replace("Series:", "").strip()
            if released_date and "Release date:" in released_date:
                released_date = released_date.replace("Release date:", "").strip()
            if ratings:
                ratings = ratings.strip()
            if language and "Language:" in language:
                language = language.replace("Language:", "").strip()
            if book_length and "Length:" in book_length:
                book_length = book_length.replace("Length:", "").strip()
            
            yield {
                "Title": book_title,
                "Book Author": book_author,
                "Narrated by": narrated_by,
                "Series": series,
                "Book Length": book_length,
                "Released Date": released_date,
                "Language": language,
                "Ratings": ratings
            }
        
        pagination =response.css('div.linkListWrapper > span >ul.pagingElements>li')
        next_page_url = pagination.css('span.nextButton a::attr(href)').get()
        if next_page_url:
            yield response.follow(url =next_page_url , callback=self.parse)

