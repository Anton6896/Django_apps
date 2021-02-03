from django.urls import path
from . import views

app_name = 'comment_api'

urlpatterns = [

    path('api/comment_create/', views.CreateCommentApi.as_view()),
    path('api/comment_list/', views.ListCommentApi.as_view()),
    path('api/comment_detail/<int:pk>/',
         views.DetailCommentApi.as_view(), name='detail'),

    # POST /api/comment_function_create/?type=mesage&pk=12
    # POST /api/comment_function_create/?type=mesage&pk=12&parent_pk=36
    path('api/comment_function_create/', views.CreateFunctionComment.as_view()),
    path('api/comment_detail_other/<int:pk>/',
         views.DetailCommentOther.as_view(), name="detail_other"),


    # search field for comment ? dont know if need for now ?
    # path('api/search_field/', views.MessageSearchFieldApi.as_view()),  # ok
]
