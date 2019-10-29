from thoth_data_collector.models import PaperItem
from rest_framework import serializers


class PaperItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PaperItem
        fields = ('paper_id', 'paper_title', 'paper_link', 'page_comments')

