# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from thoth_data_collector.models import PaperItem, PaperAuthor, PaperCategory
import urllib.request as libreq
import feedparser
import re
from dateutil.parser import parse as time_parse

@shared_task
def fetch_arxiv():
    basic_url = 'http://export.arxiv.org/api/query?'\
                'search_query=cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR'\
                '+cat:cs.NE+OR+cat:stat.ML&sortBy=lastUpdatedDate'
    start_index = 0
    max_index = 1000
    result_per_query = 100

    num_add = 0
    num_skipped = 0

    for i in range(start_index, max_index, result_per_query):
        url = basic_url + "&start=%i&max_results=%i" % (i, result_per_query)
        print(url)
        try:
            response = libreq.urlopen(url).read()
            parse = feedparser.parse(response)

            for entry in parse.entries:
                try:
                    paper_id = entry["id"]
                    if PaperItem.objects.filter(paper_id=paper_id).exists():
                        num_skipped += 1
                    else:
                        paper = PaperItem()
                        paper.paper_id = paper_id
                        paper.title = re.sub("\n+", " ", entry["title"])
                        paper.created_by = 'spider'
                        paper.created_date = time_parse(entry["published"])
                        paper.update_date = time_parse(entry["updated"])

                        for s in entry['links']:
                            if "title" in s and s["title"] == "pdf":
                                paper.paper_link = s["href"]
                        
                        paper.page_comments = entry["arxiv_comment"][:250] if "arxiv_comment" in entry else ""
                        paper.summary = re.sub("\n+", " ", entry["summary"])
                        
                        paper.save()

                        for author_name_ in entry['authors']:
                            author = PaperAuthor()
                            author.author_name = author_name_["name"]
                            author.paper_item = paper
                            author.save()

                        for category_ in entry['tags']:
                            category = PaperCategory()
                            category.paper_item = paper
                            category.term = category_["term"][:20]

                            if category_["term"] == entry["arxiv_primary_category"]["term"]:
                                category.is_primary = True
                            category.save()
                        num_add += 1
                except Exception as e:
                    print('Error when parsing the papers: ', e)

        except Exception as e:
            print('Error: ', e)
    return num_add, num_skipped

