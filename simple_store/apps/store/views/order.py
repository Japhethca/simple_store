import os
import requests
from requests.exceptions import RequestException
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class OrderSuccess(TemplateView):
    template_name = "store/pages/order-success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_details = self.request.session.get("order_details", None)
        if order_details is not None:
            context["order_number"] = order_details.get("order_number", None)
        return context

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if context.get("order_number", None) is None:
            return redirect("cart")
        return super().get(request, *args, **kwargs)


class OrderPayment(View):
    def get(self, request, **kwargs):
        return self.handle_paystack_payment(request)

    def handle_paystack_payment(self, request):
        order_details = request.session.get("order_details", None)
        if order_details is None:
            return redirect("checkout")

        payment_method = order_details.get("payment_method")
        order_amount = order_details.get("order_amount")

        paystack_secret = os.getenv("PAYSTACK_SECRET_KEY")
        paystack_api_url = os.getenv("PAYSTACK_API")
        callback_url = (
            f"{request.scheme}://{request.get_host()}{reverse('payment-success')}"
        )

        payload = {
            "email": request.user.email or f"{request.user.username}@noemail.com",
            "amount": order_amount,
            "callback_url": callback_url,
            "channels": [payment_method],
        }

        headers = {"Authorization": f"Bearer {paystack_secret}"}
        try:
            res = requests.post(paystack_api_url, json=payload, headers=headers)
            data = res.json()
        except (RequestException, ConnectionError):
            msg = "We are unable to handle transactions at this time, please try again."
            messages.add_message(
                request, messages.ERROR, message=msg, extra_tags="payment_messages"
            )

        if res.status_code == requests.codes["ok"]:
            del request.session["order_details"]
            return redirect(data["data"]["authorization_url"])

        return redirect("checkout")
