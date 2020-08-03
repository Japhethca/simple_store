from rest_framework import serializers
from django.utils.text import slugify

from simple_store.apps.core.models import Product


class ProductSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_slug(self, instance):
        return slugify(f"{instance.name}-{instance.id}")
