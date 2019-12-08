from scrapy.spiders import Spider, Request
from scrapy.selector import Selector

from collector_app.collector_app.items import TestItem
import time

class SanitySpider(Spider):
    name = 'sanity_spyder'
    allowed_domains = ['arxiv.org']
    start_urls = ['http://export.arxiv.org/api/query?'
                  'search_query=cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR'
                  '+cat:cs.NE+OR+cat:stat.ML']
    start_index = 0
    result_per_query = 500
    max_index = 10000

    def start_requests(self):

        basic_url = 'http://export.arxiv.org/api/query?'\
                    'search_query=cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR'\
                    '+cat:cs.NE+OR+cat:stat.ML&sortBy=lastUpdatedDate'
        
        for i in range(self.start_index, self.max_index, self.result_per_query):
            url = basic_url + "&start=%i&max_results=%i" % (i, self.result_per_query)
            yield Request(url=url, callback=self.parse)
            time.sleep(1)

    def parse(self, response):
        content_selector = Selector(text=response.body)
        content_selector.register_namespace('arxiv', 'http://arxiv.org/schemas/atom')
        content_selector.register_namespace('xmlns', 'http://www.w3.org/2005/Atom')
        content_selector.remove_namespaces()

        for line in content_selector.xpath('//feed/entry'):
            item = TestItem()
            item['id'] = line.xpath('id/text()').extract()
            item['title'] = line.xpath('title/text()').extract()
            item['links'] = line.xpath('link/@href').extract()
            item['authors'] = line.xpath('author/name/text()').extract()
            item['comments'] = line.xpath('comment/text()').extract()
            item['primary_category'] = line.xpath('primary_category/@term').extract()
            item['categories'] = line.xpath('category/@term').extract()
            item['summary'] = line.xpath('summary/text()').extract()
            yield item

        # i['title'] = content_selector.xpath("/feed/entry/title/text()").extract()
        # i['link'] = content_selector.xpath("/feed/entry/link/text()").extract()
        # i['author'] = content_selector.xpath("/feed/entry/author/text()")[0].extract()
