# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DpstItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    n_reviews = scrapy.Field()
    score = scrapy.Field()
    date = scrapy.Field()
    dev = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    platforms = scrapy.Field()
