# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst,MapCompose
from w3lib.html import remove_tags
class SpiderTutorialItem(scrapy.Item):
    # define the fields for your item here like:
    book_title=scrapy.Field(
        input_processor =MapCompose(remove_tags,str.strip),
        output_processor = TakeFirst()
        
        ),
    book_author=scrapy.Field(
           input_processor =MapCompose(remove_tags,str.strip),
        output_processor = TakeFirst()
        ),
    narrated_by=scrapy.Field(  
        input_processor =MapCompose(remove_tags,str.strip),
        output_processor = TakeFirst()
        ),
    series=scrapy.Field(
           input_processor =MapCompose(remove_tags,str.strip),
        output_processor = TakeFirst()
        ),
    book_length=scrapy.Field(
        input_processor =MapCompose(remove_tags,str.strip),
        output_processor = TakeFirst()
        ),
    released_date=scrapy.Field(
        input_processor =MapCompose(remove_tags,str.strip),
        output_processor = TakeFirst()
        ),
    language=scrapy.Field(  
        input_processor =MapCompose(remove_tags,str.strip),
        output_processor = TakeFirst()
        ),
    ratings=scrapy.Field(
        input_processor =MapCompose(remove_tags,str.strip),
        output_processor = TakeFirst()
    )

 
