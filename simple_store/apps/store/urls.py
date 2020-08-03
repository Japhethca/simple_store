from django.urls import path
from django.views.generic import TemplateView

from .views import home, product_detail, cart

urlpatterns = [
    path("", home, name="home"),
    path("<slug:product_id>", product_detail, name="product-details"),
    path("cart", cart, name="cart"),
]

