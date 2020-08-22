from django.urls import path

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
    OrderPaymentSuccess,
    OrderDetails,
    search,
)

urlpatterns = [
    # products
    path("", HomePage.as_view(), name="home"),
    path(
        "<slug:product_slug>-<str:product_id>",
        ProductDetail.as_view(),
        name="product-details",
    ),
    path("search", search, name="search"),
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
    path("customer/order-details/<pk>", OrderDetails.as_view(), name="order-details"),
    path(
        "order/successful/<order_number>", OrderSuccess.as_view(), name="order-success"
    ),
    path(
        "order/payment-success/<order_number>",
        OrderPaymentSuccess.as_view(),
        name="payment-success",
    ),
    path(
        "order/make-payment/<order_number>",
        OrderPayment.as_view(),
        name="make-order-payment",
    ),
    path("customer/reviews", CustomerReviews.as_view(), name="customer-reviews"),
    path("customer/favorites", CustomerFavorites.as_view(), name="customer-favorites"),
]
