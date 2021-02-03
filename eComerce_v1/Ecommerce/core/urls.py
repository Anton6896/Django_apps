from django.urls import path
from . import views

app_name = 'core'

# todo sign up redirect url not working ( update or create new user register form )

urlpatterns = [
    path('', views.HomeView.as_view(), name='item_list'),  # home
    path('product/<int:pk>/', views.ItemDetailView.as_view(), name='product'),
    path('order_summary/', views.OrderSummary.as_view(), name='order_summary'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('add_to_card/<int:pk>/', views.add_to_card, name='add_to_card'),
    path('add_coupon/', views.AddCouponView.as_view(), name='add_coupon'),
    path('refound/', views.RequestRefoundView.as_view(), name='refound'),
    path('remove_from_card/<int:pk>/',
         views.remove_from_card, name='remove_from_card'),
    path('append_to_list/<int:pk>/',
         views.append_item_tolist, name='append_tolist'),
    path('remove_from_list/<int:pk>/',
         views.remove_item_fromlist, name='remove_fromlist'),
    path('trash_item/<int:pk>/',
         views.to_trash_item, name='trash_item'),
    path('payment/<str:option>/', views.PaymentView.as_view(), name='payment'),

    
]
