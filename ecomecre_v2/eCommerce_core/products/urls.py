from django.urls import path
from .views import (
    ListOfProducts, DetailOfProduct, CreateProduct, UpdateProduct, DeleteProduct
)

app_name = 'products'

urlpatterns = [
    path("product_list/", ListOfProducts.as_view(), name="product_list"),
    path("product/<int:pk>/", DetailOfProduct.as_view(), name="product_detail"),
    path("product/<int:pk>/delete/", DeleteProduct.as_view(), name="product_delete"),
    path("product/<int:pk>/update/", UpdateProduct.as_view(), name="product_update"),
    path("product_create/", CreateProduct.as_view(), name="product_create"),

]
