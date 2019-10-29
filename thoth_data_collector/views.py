from django.shortcuts import render

# Create your views here.
from thoth_data_collector.models import PaperItem
from rest_framework import viewsets
from thoth_data_collector.serializers import PaperItemSerializer


class PaperViewSet(viewsets.ModelViewSet):
    queryset = PaperItem.objects.all().order_by('id')
    serializer_class = PaperItemSerializer

