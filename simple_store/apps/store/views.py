from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404
from simple_store.apps.core.models import Product
from .forms import SearchForm


def home(request):
    products = Product.objects.all()
    search_form = SearchForm()
    context = {"products": products, "search_form": search_form}
    return render(request, "store/pages/index.html", context=context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(
        request, "store/pages/product_details.html", context={"product": product}
    )


def cart(request):
    return render(request, "store/pages/cart.html")
