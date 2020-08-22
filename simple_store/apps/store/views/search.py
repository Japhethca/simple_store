from django.shortcuts import render
from watson import search as watson

from simple_store.apps.core.models import Product, Category


def search(request):
    context = {}
    q = request.GET.get("q")
    if q is not None:
        search_results = watson.filter(Product, q)
        context = {"search_results": search_results}
    return render(request, "store/pages/search.html", context=context)
