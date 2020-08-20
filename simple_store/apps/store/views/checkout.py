from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.contrib import messages

from simple_store.apps.core.models import (
    Cart,
    CartItem,
    BillingAddress,
    Order,
    OrderItem,
)
from ..forms import PaymentMethodForm


User = get_user_model()


class CheckoutView(LoginRequiredMixin, View):
    template_name = "store/pages/checkout.html"
    login_url = "/accounts/login"

    def get(self, request):
        cart_empty = self.get_cart_context(request).get("total_cart_price") is None
        if not request.user.is_authenticated or cart_empty:
            return redirect("cart")

        context = {
            **self.get_cart_context(request),
            "payment_form": self.get_payment_form(request),
            "default_address": self.get_default_address(request),
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        if not request.user.is_authenticated:
            print("user is not authenticated")
            return redirect("cart")

        payment_form = self.get_payment_form(request)

        delivery_add = self.get_default_address(request)
        if delivery_add is None:
            msg = "You need to select or add a delivery address"
            messages.add_message(
                request, messages.INFO, msg, extra_tags="payment_messages"
            )
            return redirect("checkout")
        if payment_form.is_valid() and delivery_add is not None:
            payment_method = payment_form.cleaned_data.get("payment_method")
            order = self.create_order(request, payment_method)
            return redirect("order-success", order_number=order.id)

        post_context = {
            **self.get_cart_context(request),
            "payment_form": payment_form,
        }

        return render(request, self.template_name, context=post_context)

    def get_cart_context(self, request):
        cart = Cart.objects.get(customer_id=request.user)
        items_in_cart = CartItem.objects.filter(cart=cart)
        total_item_price = items_in_cart.aggregate(Sum("total_price")).get(
            "total_price__sum"
        )
        return {
            "items_in_cart": items_in_cart,
            "total_cart_price": total_item_price,
        }

    def get_payment_form(self, request, **kwargs):
        form = PaymentMethodForm(prefix="payment", data=request.POST or None, **kwargs)
        return form

    def get_default_address(self, request):
        default_address = BillingAddress.objects.filter(
            customer=request.user, is_default=True
        ).first()
        if not default_address:
            default_address = BillingAddress.objects.filter(
                customer=request.user
            ).first()
            if not default_address:
                return None
            BillingAddress.set_as_default(default_address)
        return default_address

    def create_order(self, request, payment_method):
        cart = Cart.objects.get(customer_id=request.user.id)
        cart_items = CartItem.objects.filter(cart=cart)

        order = Order.objects.create(
            customer=request.user, payment_method=payment_method
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product_id,
                total_price=item.total_price,
                quantity=item.quantity,
            )

        cart_items.delete()
        return order
