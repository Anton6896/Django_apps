from django.urls import path
from . import views

app_name = 'users'
# path('', views.HomeView.as_view(), name='item_list'),  # home

urlpatterns = [
    path('register/', views.MyRegisterForm.as_view(), name='register_user'),
    
]
