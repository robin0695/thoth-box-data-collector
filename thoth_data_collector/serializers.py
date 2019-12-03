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

    def update(self, instance, validated_data):
        instance.is_recommanded = validated_data.get('is_recommanded', instance.is_recommanded)
        instance.recommand_reason = validated_data.get('recommand_reason', instance.recommand_reason)
        instance.recommand_by = validated_data.get('recommand_by', instance.recommand_by)
        instance.issue_info_id = validated_data.get('issue_info', instance.issue_info).id
        instance.save()
        return instance


class PaperAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperAuthor
        fields = ('id', 'author_name', 'author_home_page', 'author_email_addr')

class PaperSearchSerializer(HaystackSerializerMixin, PaperItemSerializer):
    class Meta(PaperItemSerializer.Meta):
        search_fields = ("text", )

        