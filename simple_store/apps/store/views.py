from django.shortcuts import render, HttpResponse, get_object_or_404, Http404, redirect
from django.http.response import HttpResponseNotFound
from django.utils.text import slugify
from django.views import View
from django.views.generic import DetailView
from simple_store.apps.core.models import Product
from .forms import SearchForm


class HomePage(View):
    form_class = SearchForm
    template_name = "store/pages/home.html"
    # http_method_names = ["GET"]

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        products = Product.objects.all()
        context = {"products": products, "search_form": form}
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

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
