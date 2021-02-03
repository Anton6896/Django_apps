from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
)
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework import permissions
from accounts.my_permissions import IsCommettee, CommentAuthor
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from . import serializers


# =========================
"""
in this way have no checking GenericForeignKey for calidation
if any of models that refers to is exists at all
"""


class CreateCommentApi(CreateAPIView):
    # comment for message
    serializer_class = serializers.CreateCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListCommentApi(ListAPIView):
    # list of all PARENT comments
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ListCommentSerializer

    def get_queryset(self):
        qs = Comment.objects.all()  # all() overridden in model
        # can attach here all search data that you like as in message section
        return qs


class DetailCommentApi(RetrieveUpdateDestroyAPIView):
    # edit / delete comment
    permission_classes = [permissions.IsAuthenticated,
                          CommentAuthor, permissions.IsAdminUser]
    # with this query set cant se the child option to edit it !
    # all() was overtired
    # queryset = Comment.objects.all()
    queryset = Comment.objects.filter(pk__gte=0)
    serializer_class = serializers.DetailCommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# =========================   OTHER WAY

"""
more proper way with validation in serializer class !
"""


class CreateFunctionComment(CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        # POST /api/comment_function_create/?type=mesage&pk=12
        # POST /api/comment_function_create/?type=mesage&pk=12&parent_pk=36
        model_type = self.request.GET.get('type')
        pk = self.request.GET.get('pk')
        parent_pk = self.request.GET.get('parent_pk', None)

        return serializers.comment_create_serializer(
            model_type=model_type,
            pk=pk,
            parent_pk=parent_pk,
            user=self.request.user
        )


# working with mixins for edit delete

class DetailCommentOther(RetrieveAPIView, DestroyModelMixin, UpdateModelMixin):
    # the all() method return only parrent comments
    permission_classes = [permissions.IsAuthenticated,
                          CommentAuthor, permissions.IsAdminUser]
    queryset = Comment.objects.filter(pk__gte=0)
    serializer_class = serializers.CommentDetailOtherSerializer

    # UpdateModelMixin
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # DestroyModelMixin
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
