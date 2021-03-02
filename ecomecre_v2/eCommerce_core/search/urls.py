from django.urls import path
from products.views import ListOfProducts
from .views import SearchProductsList

app_name = "search"

#  check the pip install django-filter
#  https://github.com/Anton6896/CarWeb/tree/master/CarDealer


urlpatterns = [
    path("", SearchProductsList.as_view(), name="search_list"),
]
