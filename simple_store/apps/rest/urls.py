from django.urls import path, re_path
from rest_framework import routers
from rest_framework.urls import url

from .views import ProductList, ProductRetrieve


urlpatterns = [
    path("products/", ProductList.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductRetrieve.as_view(), name="product-detail"),
]
