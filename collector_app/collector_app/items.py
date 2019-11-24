# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from thoth_data_collector.models import PaperItem


class CollectorAppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TestItem(scrapy.Item):

    id = scrapy.Field()
    title = scrapy.Field()
    links = scrapy.Field()
    authors = scrapy.Field()
    comments = scrapy.Field()
    primary_category = scrapy.Field()
    categories = scrapy.Field()
    summary = scrapy.Field()
