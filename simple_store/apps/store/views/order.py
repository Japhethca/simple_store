import os
import requests
from requests.exceptions import RequestException
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.conf import settings

from simple_store.apps.core.models import Order, OrderItem, ORDER_PENDING


class CustomerOrders(LoginRequiredMixin, ListView):
    template_name = "store/pages/customer-orders.html"
    login_url = "/accounts/login"
    model = Order
    context_object_name = "customer_orders"

    def get_queryset(self):
        queryset = super().get_queryset()
        orders = queryset.filter(customer=self.request.user)
        return orders


class OrderDetails(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "store/pages/order-details.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = super().get_object()
        order_items = OrderItem.objects.filter(order=order)
        order_total_price = order_items.aggregate(Sum("total_price")).get(
            "total_price__sum"
        )
        context["order_items"] = order_items
        context["order_total_price"] = order_total_price
        return context


class OrderSuccess(LoginRequiredMixin, TemplateView):
    template_name = "store/pages/order-success.html"
    login_url = "/accounts/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_number = self.kwargs.get("order_number")
        order = get_object_or_404(Order, pk=order_number)
        context["order_number"] = order.id
        return context


class OrderPayment(LoginRequiredMixin, View):
    login_url = "/accounts/login"

    def get(self, request, **kwargs):
        order_number = kwargs.get("order_number")
        return self.handle_paystack_payment(request, order_number)

    def handle_paystack_payment(self, request, order_number):
        paystack_secret = os.getenv("PAYSTACK_SECRET_KEY")
        paystack_api_url = os.getenv("PAYSTACK_API")

        order = get_object_or_404(Order, pk=order_number)
        callback_url = f"{request.scheme}://{request.get_host()}{reverse('payment-success', args=[order.id])}"

        order_amount = self.calculate_order_amount(order)
        payload = {
            "email": request.user.email or f"{request.user.username}@noemail.com",
            "amount": str(order_amount),
            "callback_url": callback_url,
            "channels": [order.payment_method],
        }

        headers = {"Authorization": f"Bearer {paystack_secret}"}
        try:
            res = requests.post(paystack_api_url, json=payload, headers=headers)
            data = res.json()
            if not res.status_code == requests.codes["ok"]:
                raise RequestException
            return redirect(data["data"]["authorization_url"])
        except (RequestException, ConnectionError):
            msg = "We are unable to handle transactions at this time, please try again."
            messages.add_message(
                request, messages.ERROR, message=msg, extra_tags="payment_messages"
            )
            return redirect("checkout")

    def calculate_order_amount(self, order):
        order_items = OrderItem.objects.filter(order=order)
        order_amount = order_items.aggregate(Sum("total_price")).get("total_price__sum")

        if settings.DEFAULT_CURRENCY["name"] == "NAIRA":
            return order_amount * 100  # convert the amount to Kobo
        return order_amount


class OrderPaymentSuccess(LoginRequiredMixin, TemplateView):
    template_name = "store/pages/payment-success.html"

    def get(self, request, *args, **kwargs):
        order_number = kwargs.get("order_number")
        order = get_object_or_404(Order, pk=order_number)
        order.status = ORDER_PENDING
        order.save()
        return super().get(request, *args, **kwargs)

