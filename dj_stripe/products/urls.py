from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('checkout_session/', views.CheckoutSessionView.as_view(), name='checkout_1'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('costume_pay/', views.StripeIntentView.as_view(), name='costume_pay'),

]
