from django.contrib import admin

from .models import (
    Category,
    Product,
    Photo,
    Brand,
    Customer,
    Review,
    Rating,
    Cart,
    CartItem,
)


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(Brand)
admin.site.register([Customer, Review, Rating, Cart, CartItem])
