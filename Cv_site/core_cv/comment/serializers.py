from rest_framework import serializers
from .models import Comment
from django.contrib.contenttypes.models import ContentType


class CreateCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = (
            "user",
            'parent',
            "content",
            "content_type",
            "object_pk",
        )


class ListCommentSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='comments:detail',
        lookup_field='pk'
    )
    user = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'detail_url',
            'replies_count',
            'id',
            'parent',
            "user",
            "timestamp",
            "content",
            "object_pk",
            "content_type",
        )

    def get_user(self, obj):
        return str(obj.user.username)

    def get_content_type(self, obj):
        return str(obj.content_type)

    def get_replies_count(self, obj):
        if obj.is_parent:
            return obj.is_child.count()
        return 0


class DetailCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    content_type = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'pk',
            "user",
            "parent",
            "content",
            "content_type",
            "object_pk",
            'replies',

        )

        read_only_fields = (
            'pk',
            'user',
            'timestamp',
            'parent',
            "object_pk",
            "content_type",
        )

    def get_content_type(self, obj):
        return str(obj.content_type)

    def get_replies(self, obj):
        if obj.is_parent:
            return ChildCommentSerializer(obj.is_child, many=True, context=self.context).data
        else:
            return None


class ChildCommentSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='comments:detail',
        lookup_field='pk'
    )

    class Meta:
        model = Comment
        fields = (
            'pk',
            "content",
            'timestamp',
            'detail_url'
        )


# ======

def comment_create_serializer(model_type='message', pk=None, parent_pk=None, user=None):
    """
    this serializer function must have an special CommentManager (models.py) function to handle it

    """

    class MyCommentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = (
                'pk',
                'content',
            )

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.pk = pk
            self.parent_obj = None
            if parent_pk:
                # double check if have an parent , if so assign to parent_obj
                qs = Comment.objects.filter(pk=parent_pk)
                if qs.exists():
                    self.parent_obj = qs.first()
            return super(MyCommentSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            """
            # because of working with the generic type of classes
            # must have an validation checks,
            # model if exist at all and check if in this model we have an instance with requeued pk
            """

            model_qs = ContentType.objects.filter(model=self.model_type)
            if not model_qs.exists():
                print(ContentType.objects.all())
                raise serializers.ValidationError(
                    'PROBLEM -> with model_qs in validation ... cant find model ')
            obj_model = model_qs.first().model_class()
            obj_qs = obj_model.objects.filter(pk=self.pk)
            if not obj_qs.exists():
                raise serializers.ValidationError(
                    'PROBLEM -> obj_qs in validation ... cant find object ')
            return data

        def create(self, validated_data):
            comment = Comment.objects.create_by_model_type(
                model_type=self.model_type,
                pk=self.pk,
                content=validated_data.get("content"),
                user=user,
                parent_obj=self.parent_obj
            )
            return comment

    return MyCommentSerializer


class CommentDetailOtherSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'pk',
            'user',
            'content',
            'timestamp',
            'parent',
            'replies',


        )
        read_only_fields = (
            'pk',
            'user',
            'timestamp',
            'parent',

        )

    def get_user(self, obj):
        return str(obj.user.username)

    def get_replies(self, obj):
        if obj.is_parent:
            return ChildCommentSerializer(obj.is_child, many=True, context=self.context).data
        else:
            return None
