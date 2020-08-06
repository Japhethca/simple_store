from django.shortcuts import render, HttpResponse, get_object_or_404, Http404, redirect
from django.http.response import HttpResponseNotFound
from django.utils.text import slugify

from simple_store.apps.core.models import Product
from .forms import SearchForm


def home(request):
    products = Product.objects.all()
    search_form = SearchForm()
    context = {"products": products, "search_form": search_form}
    return render(request, "store/pages/home.html", context=context)


def product_detail(request, product_slug, product_id):
    try:
        int(product_id)
    except ValueError:
        raise Http404()

    product = get_object_or_404(Product, pk=product_id)
    if (slug := slugify(product.name)) != product_slug:
        return redirect("product-details", slug, product.id)

    return render(
        request, "store/pages/product_details.html", context={"product": product}
    )


def cart(request):
    return render(request, "store/pages/cart.html")
