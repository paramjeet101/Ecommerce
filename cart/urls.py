from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("", CartView.as_view()),
    path("add/", AddToCartAPI.as_view()),
    path("update/<int:item_id>/", UpdateCartItemAPI.as_view()),
    path("remove/<int:item_id>/", RemoveCartItemAPI.as_view()),
    path("clear/", ClearCartAPI.as_view()),
]
