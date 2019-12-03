from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

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

class PaperSearchView(HaystackViewSet):
    index_models = [PaperItem]
    serializer_class = PaperSearchSerializer
    permission_classes = []


def paper_like(request, id, value):
    paper = get_object_or_404(PaperItem, id=id)
    paper.like_count += int(value)
    paper.save()
    return JsonResponse({"status": 200})

    


