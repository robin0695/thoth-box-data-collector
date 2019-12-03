from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from thoth_data_collector.models import PaperItem, PaperAuthor, IssueInfo
from rest_framework import viewsets
from thoth_data_collector.serializers import PaperItemSerializer, PaperAuthorSerializer, IssueInfoSerializer, PaperSearchSerializer
from rest_framework import generics
from django.views import View
from haystack.query import SearchQuerySet
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.permissions import IsAuthenticated

class PaperViewSet(viewsets.ModelViewSet):
    queryset = PaperItem.objects.all().order_by('-id')
    serializer_class = PaperItemSerializer


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
        return queryset

class PaperSearchView_V2(View):
    template_name = 'search/search.html'
    sqs = SearchQuerySet()

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', None)
        if query is not None:
            results = self.sqs.filter(content=query).models(PaperItem)
        else:
            results = self.sqs.all()
        
        papers = [r.object for r in results]
        return render(request, self.template_name, {'papers': papers})

class PaperSearchView(HaystackViewSet):
    index_models = [PaperItem]
    serializer_class = PaperSearchSerializer
    permission_classes = []

