# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoodItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'goods'
    name = scrapy.Field()
    price = scrapy.Field()
    comment = scrapy.Field()
    shop = scrapy.Field()
