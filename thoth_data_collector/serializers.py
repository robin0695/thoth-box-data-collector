from thoth_data_collector.models import PaperItem, PaperAuthor, PaperCategory
from rest_framework import serializers


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
                  'recommand_by', 'authors', 'categories')

    def update(self, instance, validated_data):
        instance.is_recommanded = validated_data.get('is_recommanded', instance.is_recommanded)
        instance.recommand_reason = validated_data.get('recommand_reason', instance.recommand_reason)
        instance.recommand_by = validated_data.get('recommand_by', instance.recommand_by)
        instance.save()
        return instance


class PaperAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperAuthor
        fields = ('id', 'author_name', 'author_home_page', 'author_email_addr')
