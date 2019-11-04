from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from thoth_data_collector.models import PaperItem, PaperAuthor
from rest_framework import viewsets
from thoth_data_collector.serializers import PaperItemSerializer, PaperAuthorSerializer


class PaperViewSet(viewsets.ModelViewSet):
    queryset = PaperItem.objects.all().order_by('id')
    serializer_class = PaperItemSerializer


class PaperAuthorViewSet(viewsets.ModelViewSet):
    queryset = PaperAuthor.objects.all().order_by('id')
    serializer_class = PaperAuthorSerializer

