from django.urls import path
from . import views

app_name = 'cart'

# path('cart/', include('carts.urls')),
urlpatterns = [
    path('', views.cart_home, name='cart_home'),
    path('update/', views.cart_update, name='cart_update'),
    path('checkout/', views.CheckOutView.as_view(), name='cart_checkout'),
    path('payment_redirect/<int:pk>/', views.PayStripe.as_view(), name='payment_redirect'),
    path('delete_from_cart/', views.delete_from_cart, name='delete_from_cart'),

    # stripe
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]
