from django.http.response import JsonResponse, HttpResponseNotAllowed
from rest_framework import generics

from simple_store.apps.core.models import Product
from .serializers import ProductSerializer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieve(generics.RetrieveAPIView):
    queryset = Product
    serializer_class = ProductSerializer
