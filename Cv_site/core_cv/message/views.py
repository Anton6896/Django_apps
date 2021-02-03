"""
Pagination is set by default to 10 in settings
2 section messages and comments (i live them in one place)
"""
from django.views.generic import View
from django.shortcuts import render
from rest_framework import permissions
from accounts.my_permissions import ObjOwner
from .models import Mesage
from django.db.models import Q
from . import serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
)


# ===========================  blog html section
# todo blog as html version with comments
class BlogHome(View):
    def get(self, *args, **kwarg):
        return render(self.request, 'message_grid.html')


# ===========================  Message section
class MessageCreateApi(CreateAPIView):
    """
    on crete have signal that check if instance == message -> status = done
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CreateMessageSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MessageDetailApi(RetrieveUpdateDestroyAPIView):
    # using for message and for issue as one (retrieve, update, delete )
    permission_classes = [permissions.IsAuthenticated, ObjOwner]
    serializer_class = serializers.EditMessageSerializer
    queryset = Mesage.objects.all()


class MessageListApi(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ListMessageSerializer
    queryset = Mesage.objects.filter(tag='message').filter(is_read=False).all()


class IssueMessageListApi(ListAPIView):
    # list of all issues (queryset -> issue tag, working_on, on_hold )
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ListMessageSerializer
    queryset = Mesage.objects.filter(tag='issue').filter(status='working_on').all()


class MessageSearchFieldApi(ListAPIView):
    # look thru the search field q or search

    # /api/search_field/?search= question
    # /api/search_field/?q= question
    # /api/search_field/?search=question&q= question
    # /api/search_field/?search=21&ordering=-title
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.EditMessageSerializer
    filter_backends = [SearchFilter, OrderingFilter, ]
    search_fields = ['title', 'author__username', 'content', 'status', 'tag']

    def get_queryset(self):
        queryset = Mesage.objects.all()
        q = self.request.GET.get('q', None)
        if q:
            # using Q library for multi queryset
            queryset = Mesage.objects.filter(
                Q(title__icontains=q) |
                Q(author__username=q) |
                Q(content__icontains=q) |
                Q(status=q) |
                Q(tag=q)
            ).distinct()

        return queryset
