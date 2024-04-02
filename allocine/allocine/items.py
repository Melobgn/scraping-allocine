# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AllocineItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    years_career = scrapy.Field()
    number_films_series = scrapy.Field()
    
