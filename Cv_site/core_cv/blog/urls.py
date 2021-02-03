from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
    path("blog/", views.ListOfPosts.as_view(), name="blog_list"),
    path("blog/<int:pk>/", views.DetailPost.as_view(), name="blog_detail"),
    path("create_blog/", views.CreatePost.as_view(), name="blog_create"),
]
