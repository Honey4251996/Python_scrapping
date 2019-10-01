# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GsmarenaScraperItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    images = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    data = scrapy.Field()
