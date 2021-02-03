from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from django.views import generic  # class view
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class PostDetailView(generic.DetailView):
    model = Post
    # for template_name -> will django is expect for <app>/<model>_<viewtype>.html


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    # create new post only if user is authenticated
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request, f'Post created for {self.request.user.username}')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    # update new post only if user is authenticated
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request, f'Post Updated for {self.request.user.username}')
        return super().form_valid(form)

    def test_func(self):
        # check if the user is author of this post
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        # check if the user is author of this post
        post = self.get_object()
        return self.request.user == post.author


class UserPostListView(generic.ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    username = '' # i want set title with this user name 

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        usermane = user.username # for title 
        # limit this class to use only posts with this user or 404
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Your Posts'
        return context
