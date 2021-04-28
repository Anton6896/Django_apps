from django.urls import path
from .views import payment_view

app_name = "billing"

urlpatterns = [
    path("", payment_view, name="payment_page")
]
