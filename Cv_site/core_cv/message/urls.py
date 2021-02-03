from django.urls import path
from . import views

app_name = 'message_api'

urlpatterns = [
    # http
    path('blog_home/', views.BlogHome.as_view(), name='blog_home'),

    # crud
    path('api/message_create/', views.MessageCreateApi.as_view()),  # ok
    path('api/message_detail/<int:pk>/', views.MessageDetailApi.as_view(), name='detail'),  # ok
    # see all messages/issues  , comments for them
    path('api/message_list/', views.MessageListApi.as_view()),  # ok
    path('api/issue_list/', views.IssueMessageListApi.as_view()),  # ok
    # search field look up
    path('api/search_field/', views.MessageSearchFieldApi.as_view()),  # ok
]
