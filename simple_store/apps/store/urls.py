from django.urls import path
from django.views.generic import TemplateView

from .views import (
    HomePage,
    ProductDetail,
    CartView,
    CartItemDelete,
    CheckoutView,
    CustomerProfile,
    CustomerAddress,
    CustomerOrders,
    CustomerReviews,
    CustomerFavorites,
    CatalogView,
    CategoryView,
    CustomerAddressNew,
    CustomerAddressDelete,
    CustomerAddressSetDefault,
    OrderSuccess,
    OrderPayment,
)

urlpatterns = [
    # products
    path("", HomePage.as_view(), name="home"),
    path(
        "<slug:product_slug>-<str:product_id>",
        ProductDetail.as_view(),
        name="product-details",
    ),
    path("catalog", CatalogView.as_view(), name="catalog"),
    path("c/<slug:category_name>", CategoryView.as_view(), name="category-products"),
    # cart
    path("cart", CartView.as_view(), name="cart"),
    path("cart/item-delete/<pk>", CartItemDelete.as_view(), name="cart-item-delete"),
    # checkout
    path("checkout", CheckoutView.as_view(), name="checkout"),
    # customers
    path("customer", CustomerProfile.as_view(), name="customer"),
    path("customer/profile", CustomerProfile.as_view(), name="customer-profile"),
    path("customer/address", CustomerAddress.as_view(), name="customer-address"),
    path(
        "customer/address/new",
        CustomerAddressNew.as_view(),
        name="customer-address-new",
    ),
    path(
        "customer/address/edit/<pk>",
        CustomerAddressNew.as_view(),
        name="customer-address-edit",
    ),
    path(
        "customer/address/remove/<pk>",
        CustomerAddressDelete.as_view(),
        name="customer-address-delete",
    ),
    path(
        "customer/address/set-default/<pk>",
        CustomerAddressSetDefault.as_view(),
        name="customer-address-set-default",
    ),
    path("customer/orders", CustomerOrders.as_view(), name="customer-orders"),
    path("order/successful", OrderSuccess.as_view(), name="order-success"),
    path("customer/reviews", CustomerReviews.as_view(), name="customer-reviews"),
    path("customer/favorites", CustomerFavorites.as_view(), name="customer-favorites"),
    path(
        "payment/payment-success",
        TemplateView.as_view(template_name="store/pages/payment-success.html"),
        name="payment-success",
    ),
    path(
        "payment/make-order-payment", OrderPayment.as_view(), name="make-order-payment",
    ),
]
