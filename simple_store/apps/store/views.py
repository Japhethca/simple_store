from django.shortcuts import (
    render,
    HttpResponse,
    get_object_or_404,
    Http404,
    redirect,
    reverse,
)
from django.urls import reverse_lazy
from django.http.request import QueryDict
from django.http.response import HttpResponseNotFound
from django.utils.text import slugify
from django.views import View
from django.views.generic import DetailView, DeleteView
from django.db.models import Sum

from simple_store.apps.core.models import Product, Cart, CartItem
from .forms import SearchForm


class HomePage(View):
    form_class = SearchForm
    template_name = "store/pages/home.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        products = Product.objects.all()
        context = {
            "products": products,
            "search_form": form,
        }
        return render(request, self.template_name, context=context)


class ProductDetail(DetailView):
    template_name = "store/pages/product_details.html"
    model = Product
    context_object_name = "product"
    pk_url_kwarg = "product_id"

    def get(self, request, **kwargs):
        product_slug = kwargs.get("product_slug")
        product_id = kwargs.get("product_id")
        try:
            int(product_id)
        except ValueError:
            raise Http404()

        product = self.get_object()
        if (slug := slugify(product.name)) != product_slug:
            return redirect("product-details", slug, product.id)

        return super().get(request, **kwargs)


class CartView(View):
    http_method_names = ["get", "post", "put"]
    template_name = "store/pages/cart.html"

    def get(self, request, **kwargs):
        context = {}
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(customer_id=request.user.id)
            cart_items = CartItem.objects.filter(cart=cart)
            cart_total = cart_items.aggregate(Sum("total_price"))
            context["cart_items"] = cart_items
            context["cart_items_total"] = cart_total.get("total_price__sum")
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
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
