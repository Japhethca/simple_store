"""
Cart views
"""
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
)
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.http.request import QueryDict
from django.views import View
from django.views.generic import DeleteView
from django.db.models import Sum

from simple_store.apps.core.models import (
    Product,
    Cart,
    CartItem,
)


User = get_user_model()


class CartView(View):
    http_method_names = ["get", "post", "put"]
    template_name = "store/pages/cart.html"

    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(customer_id=request.user.id)
            cart_items = CartItem.objects.filter(cart=cart)
            cart_total = cart_items.aggregate(Sum("total_price"))

            context["cart_items"] = cart_items
            context["cart_items_total"] = cart_total.get("total_price__sum")
        return render(request, self.template_name, context=context)

    def post(self, request):
        if not request.user.is_authenticated:
            querydict = QueryDict(request.META.get("QUERY_STRING"))
            next_url = querydict.get("next", "/")
            url = reverse("account_login") + f"?next={next_url}"
            return redirect(url)

        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, pk=product_id)

        cart, _ = Cart.objects.get_or_create(customer_id=request.user)
        try:
            cart_item = CartItem.objects.get(product_id=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product_id=product, cart=cart, price=product.price
            )

        return redirect("cart")


class CartItemDelete(DeleteView):
    model = CartItem
    success_url = reverse_lazy("cart")
