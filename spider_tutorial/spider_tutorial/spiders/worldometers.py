# from gc import callbacks
# from turtle import title
# import scrapy

# class WorldometersSpider(scrapy.Spider):
#     name = "worldometers"
#     allowed_domains = ["www.worldometers.info"]
#     start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

#     def parse(self, response):
#         title = response.xpath('//h1/text()').get()
#         countries = response.xpath('//td/a')
#         for country in countries:
#             country_name = country.xpath('.//text()').get()
#             link = country.xpath('.//@href').get()

#             # Absolute Url
#             # absolute_url = f'https://www.worldometers.info/{link}'
#             absolute_url = response.urljoin(link)

#             yield response.follow(url=absolute_url, callback=self.parse_country, meta={'country': country_name})

#     def parse_country(self, response):
#         country = response.request.meta['country']
#         rows = response.xpath("(//table[contains(@class,'table')])[1]/tbody/tr")
#         for row in rows:
#             year = row.xpath(".//td[1]/text()").get()
#             population = row.xpath(".//td[2]/strong/text()").get()
#             yield {
#                 'year': year,
#                 'population': population,
#                 'country': country
#             }
"""The following is using css selector"""
from gc import callbacks
from turtle import title
import scrapy

class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        title = response.css('h1::text').get()
        countries = response.css('td a')
        for country in countries:
            country_name = country.css('::text').get()
            link = country.css('::attr(href)').get()

            # Absolute Url
            absolute_url = response.urljoin(link)

            yield response.follow(url=absolute_url, callback=self.parse_country, meta={'country': country_name})

    def parse_country(self, response):
        country = response.request.meta['country']
        rows = response.css("table.table tbody tr")
        for row in rows:
            year = row.css("td:nth-child(1)::text").get()
            population = row.css("td:nth-child(2) strong::text").get()
            yield {
                'year': year,
                'population': population,
                'country': country
            }
