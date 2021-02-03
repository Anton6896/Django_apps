from rest_framework import serializers
from .models import Mesage
from comment.serializers import ListCommentSerializer, DetailCommentSerializer
from comment.models import Comment


class CreateMessageSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    title = serializers.CharField(required=True, max_length=200)
    tag = serializers.ChoiceField(choices=Mesage.TAG_CHOICES,
                                  default='message')
    status = serializers.ChoiceField(choices=Mesage.STATUS_CHOICES,
                                     default='working_on')

    class Meta:
        model = Mesage
        fields = (
            'author',
            'title',
            'image',
            'content',
            'priority',
            'tag',
            'status',
        )


class EditMessageSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # title = serializers.CharField(required=True, max_length=200)
    tag = serializers.ChoiceField(choices=Mesage.TAG_CHOICES,
                                  default='message')
    status = serializers.ChoiceField(choices=Mesage.STATUS_CHOICES,
                                     default='working_on')
    pk = serializers.IntegerField(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Mesage
        fields = (
            'pk',
            'author',
            'title',
            'image',
            'content',
            'priority',
            'tag',
            'status',
            'is_read',
            'comments',

        )

    def get_comments(self, obj):
        # this two already done in model Comment "filter_by_instance"
        # content_type = obj.get_content_type
        # object_id = obj.pk
        comments = Comment.objects.filter_by_instance(obj)
        data = ListCommentSerializer(comments, many=True, context=self.context).data
        return data


class ListMessageSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='messages:detail',
        lookup_field='pk',
    )
    author = serializers.SerializerMethodField()
    html = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Mesage
        fields = (
            'pk',
            'detail_url',
            'author',
            'title',
            'image',
            'content',
            'priority',
            'html',
            'status',
            "comments_count",
        )

    def get_html(self, obj):
        return obj.get_markdown()

    def get_author(self, obj):
        # author = serializers.SerializerMethodField()
        return str(obj.author.username)

    def get_comments_count(self, obj):
        sum = Comment.objects.filter(object_pk=obj.pk).count()
        return sum
