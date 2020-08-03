from django.contrib import admin

from .models import Category, Product, Photo, Brand


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(Brand)
