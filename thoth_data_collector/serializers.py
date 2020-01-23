from thoth_data_collector.models import PaperItem, PaperAuthor, PaperCategory, IssueInfo
from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializerMixin
from thoth_data_collector.search_indexes import PaperItemIndex
from django.contrib.auth import get_user_model  # If used custom user model


class IssueInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueInfo
        fields = ('id', 'issue_title', 'issue_date', 'issue_sn',
                  'update_date', 'update_by', 'is_deleted')


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
                  'recommand_by', 'authors', 'categories', 'issue_info', 'summary', 'like_count', 'view_count', 'code_url')


class PaperAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperAuthor
        fields = ('id', 'author_name', 'author_home_page', 'author_email_addr')


class PaperSearchSerializer(HaystackSerializerMixin, PaperItemSerializer):
    class Meta(PaperItemSerializer.Meta):
        search_fields = ("text", )


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ['url', 'username', 'email', 'groups', 'password', 'last_login',
                  'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'is_superuser']

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            last_login=validated_data['last_login'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=validated_data['is_staff'],
            is_active=validated_data['is_active'],
            date_joined=validated_data['date_joined'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
