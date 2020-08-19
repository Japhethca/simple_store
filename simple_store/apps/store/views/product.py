"""
Product views
"""

from django.shortcuts import (
    get_object_or_404,
    Http404,
    redirect,
)
from django.utils.text import slugify
from django.views.generic import DetailView, ListView

from simple_store.apps.core.models import (
    Product,
    Category,
)


class HomePage(ListView):
    model = Product
    template_name = "store/pages/home.html"
    context_object_name = "products"


class ProductDetail(DetailView):
    template_name = "store/pages/product_details.html"
    model = Product
    context_object_name = "product"
    pk_url_kwarg = "product_id"

    def get(self, request, *arg, **kwargs):
        product_slug = kwargs.get("product_slug")
        product_id = kwargs.get("product_id")
        try:
            int(product_id)
        except ValueError:
            raise Http404()

        product = self.get_object()
        if (slug := slugify(product.name)) != product_slug:
            return redirect("product-details", slug, product.id)

        return super().get(request, *arg, **kwargs)


class CatalogView(ListView):
    template_name = "store/pages/catalog.html"
    queryset = Product.objects.all()
    context_object_name = "products"


class CategoryView(ListView):
    template_name = "store/pages/category.html"
    queryset = Product.objects.all()
    context_object_name = "category_products"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_name = ""

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get("category_name")
        self.category_name = " ".join(category_slug.split("-"))
        category = get_object_or_404(Category, name__icontains=self.category_name)
        cat_products = queryset.filter(categories=category)
        return cat_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_name"] = self.category_name
        return context
