# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyPoolItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    protocol = scrapy.Field()
    website = scrapy.Field()
    address = scrapy.Field()
    score = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
    types = scrapy.Field()
