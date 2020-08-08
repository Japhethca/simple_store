from django.urls import path
from django.views.generic import TemplateView

from .views import HomePage, ProductDetail, CartView

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path(
        "<slug:product_slug>-<str:product_id>",
        ProductDetail.as_view(),
        name="product-details",
    ),
    path("cart", CartView.as_view(), name="cart"),
]

