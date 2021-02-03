from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.About.as_view(), name='about'),
    path('result/', views.FilterResults.as_view(), name='filter'),
    path('car_detail/<int:pk>/', views.CarDetail.as_view(), name='car_detail'),  
    path('inventory/', views.InventoryList.as_view(), name='inventory'),

]
