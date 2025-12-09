from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("categories/", CategoryListCreateAPI.as_view(), name="category_list_create"),
    path("categories/<int:pk>/", CategoryDetailAPI.as_view(), name="category_detail"),

    # PRODUCT
    path("products-list/", ProductListCreateAPI.as_view(), name="product_list_create"),
    path("products/<int:pk>/", ProductDetailAPI.as_view(), name="product_detail"),
]
