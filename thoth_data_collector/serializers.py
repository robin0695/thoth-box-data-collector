from thoth_data_collector.models import PaperItem, PaperAuthor, PaperCategory, IssueInfo
from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializerMixin
from thoth_data_collector.search_indexes import PaperItemIndex

class IssueInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueInfo
        fields = ('id', 'issue_title', 'issue_date', 'issue_sn', 'update_date', 'update_by', 'is_deleted')


class PaperCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperCategory
        fields = ('id', 'term', 'is_primary')


class PaperItemSerializer(serializers.ModelSerializer):
    authors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='author_name'
    )

    categories = PaperCategorySerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = PaperItem
        fields = ('id', 'paper_id', 'paper_title', 'paper_link', 'page_comments', 'is_recommanded', 'recommand_reason',
                  'recommand_by', 'authors', 'categories', 'issue_info', 'summary', 'like_count', 'view_count')

class PaperAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperAuthor
        fields = ('id', 'author_name', 'author_home_page', 'author_email_addr')

class PaperSearchSerializer(HaystackSerializerMixin, PaperItemSerializer):
    class Meta(PaperItemSerializer.Meta):
        search_fields = ("text", )

        