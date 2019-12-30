import os
import shutil
import urllib.request as libreq

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from drf_haystack.viewsets import HaystackViewSet
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views, parsers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.db import transaction
from paper_process.tasks import paper_process_pipeline, pdf2html

from thoth_data_collector.models import PaperItem, PaperAuthor, IssueInfo, PaperCategory
from thoth_data_collector.serializers import PaperItemSerializer, PaperAuthorSerializer, IssueInfoSerializer, \
    PaperSearchSerializer
from urllib.parse import quote
import urllib.request as libreq
import feedparser
import re

from scrapy.selector import Selector
from collector_app.collector_app.items import TestItem


class PaperViewSet(viewsets.ModelViewSet):
    queryset = PaperItem.objects.all().order_by('-created_date')
    serializer_class = PaperItemSerializer
    filterset_fields = ['is_recommanded']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.view_count += 1
        instance.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def paper_like(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like_count += 1
        instance.save()
        return Response({'status': 'like confirmed', 'like_count': instance.like_count})

    @action(detail=True, methods=['patch'])
    def paper_recommand(self, request, *args, **kwargs):
        instance = self.get_object()

        is_recommanded = instance.is_recommanded

        if is_recommanded:
            return Response({'status': 200, 'message': "The paper has already been recommanded."})

        # download the pdf
        pdf_url = instance.paper_link

        # transform the pdf
        paper_process_pipeline.delay(pdf_url, settings.HTML_ROOT)

        # save the data
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 200, 'message': "Successfully Recommand %s" % instance.paper_title})


class PaperAuthorViewSet(viewsets.ModelViewSet):
    queryset = PaperAuthor.objects.all().order_by('id')
    serializer_class = PaperAuthorSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = IssueInfo.objects.all().order_by('-id')
    serializer_class = IssueInfoSerializer


class RecommandPaperList(generics.ListAPIView):
    serializer_class = PaperItemSerializer

    def get_queryset(self):
        isRecommanded = self.request.query_params.get('is_recommanded', None)
        if isRecommanded is not None:
            queryset = PaperItem.objects.filter(is_recommanded=isRecommanded)
        else:
            queryset = PaperItem.objects.all()
        return queryset.order_by("-update_date")


class PaperSearchView(HaystackViewSet):
    index_models = [PaperItem]
    serializer_class = PaperSearchSerializer
    permission_classes = []


@permission_classes((permissions.AllowAny,))
class FileUploadView(views.APIView):
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    serializer_class = PaperItemSerializer

    @csrf_exempt
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        print(request.data['file'])
        print(request.data)
        data_folder = os.path.join(settings.MEDIA_ROOT, 'pdfs')
        output_paper_file = os.path.join(
            data_folder, request.data['file'].name)

        with open(output_paper_file, "wb") as fp:
            shutil.copyfileobj(request.data['file'], fp)

        try:
            paper_item = PaperItem.objects.get(
                paper_id=request.data["paper_id"])
        except PaperItem.DoesNotExist:

            newPaper = PaperItem()
            newPaper.is_recommanded = True
            newPaper.issue_info = IssueInfo.objects.get(
                pk=request.data['issue_info'])
            newPaper.paper_id = request.data["paper_id"]
            newPaper.paper_title = request.data["paper_title"]
            newPaper.paper_link = request.data["paper_link"]
            newPaper.page_comments = request.data["paper_comments"]
            newPaper.summary = request.data["paper_summary"]
            newPaper.recommand_reason = request.data["recommand_reason"]
            newPaper.created_by = "upload"
            newPaper.save()

            authors = request.data["paper_authors"].split('|')
            for author in authors:
                newAuthor = PaperAuthor()
                newAuthor.author_name = author
                newAuthor.paper_item = newPaper
                newAuthor.save()
            # transform the pdf to html
            pdf2html.delay(output_paper_file, settings.HTML_ROOT)

        return Response(request.data, status=status.HTTP_201_CREATED)


@permission_classes((permissions.AllowAny,))
class AddOldArchivePaper(views.APIView):
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def saveItem2Db(self, item):
        paper_id = item['id'][0]
        # check if paper exisits in data
        if PaperItem.objects.filter(paper_id=paper_id).exists():
            print("File already there")
            return
        else:
            paperItem = PaperItem()

            paperItem.paper_id = item['id'][0]
            paperItem.paper_title = item['title'][0]
            paperItem.created_by = 'admin'

            for s in item['links']:
                if 'pdf' in s:
                    paperItem.paper_link = s
            paperItem.page_comments = item['comments'][0] if len(
                item["comments"]) > 0 else ""
            paperItem.summary = item['summary'][0] if len(
                item["summary"]) > 0 else ""
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

    @csrf_exempt
    def put(self, request, *args, **kwargs):
        archive_url = 'http://export.arxiv.org/api/query?id_list=' + \
            request.data['old_paper_id']
        print(archive_url)
        with libreq.urlopen(archive_url) as url:
            r = url.read()
            content_selector = Selector(text=r)
            content_selector.register_namespace(
                'arxiv', 'http://arxiv.org/schemas/atom')
            content_selector.register_namespace(
                'xmlns', 'http://www.w3.org/2005/Atom')
            content_selector.remove_namespaces()

            for line in content_selector.xpath('//feed/entry'):
                item = TestItem()
                item['id'] = line.xpath('id/text()').extract()
                item['title'] = line.xpath('title/text()').extract()
                item['links'] = line.xpath('link/@href').extract()
                item['authors'] = line.xpath('author/name/text()').extract()
                item['comments'] = line.xpath('comment/text()').extract()
                item['primary_category'] = line.xpath(
                    'primary_category/@term').extract()
                item['categories'] = line.xpath('category/@term').extract()
                item['summary'] = line.xpath('summary/text()').extract()
                self.saveItem2Db(item)

        return Response(item, status=status.HTTP_201_CREATED)


@permission_classes((permissions.AllowAny,))
class ArxivSearchView(views.APIView):
    def get(self, request, *args, **kwargs):
        base_url = "http://export.arxiv.org/api/query?sortBy=lastUpdatedDate&start=0&max_results=50&search_query="

        #query_term = "(cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML)+AND+("
        q = request.query_params["query"].replace(" ", "+")

        query_term = ""
        terms = ["ti", "au"]
        for i, t in enumerate(terms):
            query_term += '%s:"%s"' % (t, q)
            if i != len(terms)-1:
                query_term += "+OR+"

        url = base_url + query_term
        print('search url: %s' % url)
        response = libreq.urlopen(url).read()
        parse = feedparser.parse(response)

        results = {"results": [], "count": len(parse.entries)}
        for entry in parse.entries:
            paper_link = ""
            for s in entry['links']:
                if "title" in s and s["title"] == "pdf":
                    paper_link = s["href"]

            authors = [author["name"] for author in entry["authors"]]
            categories = [{"term": c["term"][:20], "is_primary": c["term"] ==
                           entry["arxiv_primary_category"]["term"]} for c in entry["tags"]]

            paper = {
                "paper_id": entry["id"],
                "paper_title": re.sub("\n+", " ", entry["title"]),
                "paper_link": paper_link,
                "page_comments": entry["arxiv_comment"][:250] if "arxiv_comment" in entry else "",
                "summary": re.sub("\n+", " ", entry["summary"]),
                "authors": authors,
                "categories": categories
            }
            results["results"].append(paper)

        return Response(data=results, status=200)
