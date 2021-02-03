from django.urls import path
from . import views

# app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='blog-post-detail'),
    path('post/create/', views.PostCreateView.as_view(), name='blog-post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='blog-post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='blog-post-delete'),
    path('user/<str:username>', views.UserPostListView.as_view(), name='blog-user-posts')
]
