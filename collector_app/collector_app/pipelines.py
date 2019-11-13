# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from thoth_data_collector.models import PaperItem
from thoth_data_collector.models import PaperAuthor
from thoth_data_collector.models import PaperCategory


class CollectorAppPipeline(object):

    def process_item(self, item, sanityspyder):

        paperItem = PaperItem()

        paperItem.paper_id = item['id'][0]
        paperItem.paper_title = item['title'][0]
        paperItem.created_by = 'spider'

        for s in item['links']:
            if 'pdf' in s:
                paperItem.paper_link = s
        paperItem.page_comments = item['comments'][0]
        paperItem.summary = item['summary'][0]
        paperItem.save()

        for author_name_ in item['authors']:
            author = PaperAuthor()
            author.author_name = author_name_
            author.paper_item = paperItem
            author.save()

        for category_ in item['categories']:
            category = PaperCategory()
            category.paper_item = paperItem
            category.term = category_
            if category_ == item['primary_category'][0]:
                category.is_primary = True
            category.save()

        return item
