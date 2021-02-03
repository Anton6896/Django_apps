
from os import name
from os.path import commonpath
from django.contrib.admin.options import csrf_protect_m
from django.shortcuts import render
from django.views import generic
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from . import forms
from django.http import HttpResponseRedirect


class ListOfPosts(generic.ListView):
    model = models.Blog
    context_object_name = 'blogs_list'
    template_name = "blog_list.html"
    paginate_by = 3

    def get_queryset(self):
        return models.Blog.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ListOfPosts, self).get_context_data(**kwargs)
        context['title'] = 'Blog'
        return context


class CreatePost(LoginRequiredMixin, generic.CreateView):
    model = models.Blog
    template_name = "create_blog_mess.html"

    fields = [
        'title',
        'content',
        'image',
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user

        messages.success(
            self.request, f'Post created for {self.request.user.username}')

        return super().form_valid(form)


class DetailPost(generic.detail.DetailView):
    model = models.Blog
    template_name = "blog_detail.html"
    context_object_name = 'blog'
    comment_form = forms.CommentForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = "Blog Detail"
        context['form'] = self.comment_form

        return context

    def post(self, *args, **kwargs):

        form = self.comment_form = forms.CommentForm(self.request.POST or None)

        if form.is_valid():
            user = self.request.user
            blog = models.Blog.objects.filter(pk=self.kwargs['pk']).first()
            content = form.cleaned_data.get('content')

            new_comment, created = models.BlogComment.objects.get_or_create(
                blog=blog,
                author=user,
                content=content
            )

            if created:
                print("------------------   working ")

        return HttpResponseRedirect('.')  # <- stay on this page
