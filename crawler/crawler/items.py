# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class News(scrapy.Item):
    href = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()

class MainNews(News):
    sub = scrapy.Field()
    related = scrapy.Field()
