# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SspItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    article_id = scrapy.Field()
    url = scrapy.Field()
    article_time = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    keywords = scrapy.Field()
    c_time = scrapy.Field()
