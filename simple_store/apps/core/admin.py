from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.conf import settings
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
    Order,
    OrderItem,
    User,
)

site_currency_symbol = settings.DEFAULT_CURRENCY.get("symbol")


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        fields = ("email", "date_of_birth", "phone_number", "is_active", "is_admin")

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "first_name", "last_name", "is_admin")
    list_filter = ("is_admin",)

    fieldsets = (
        (
            None,
            {"fields": ("email", "username", "first_name", "last_name", "password")},
        ),
        ("Personal info", {"fields": ("phone_number", "date_of_birth")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )

    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("email", "password1", "password2",),},
        ),
        (
            "Other info (not required)",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "phone_number",
                    "date_of_birth",
                )
            },
        ),
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "product_price", "brand", "published")
    search_fields = ("name", "description")

    def product_price(self, obj):

        return f"{site_currency_symbol}{obj.price}"

    product_price.short_description = "Price"


class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_number", "cart_owner")

    def cart_number(self, obj):
        return obj.id

    cart_number.short_description = "Cart ID"

    def cart_owner(self, obj):
        return obj.customer_id.email

    cart_number.short_description = "Cart Owner"


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("product_name", "quantity", "item_total_price", "cart_owner")

    def product_name(self, obj):
        return obj.product_id.name

    product_name.short_description = "Product Name"

    def item_total_price(self, obj):
        return f"{site_currency_symbol}{obj.total_price}"

    item_total_price.short_description = "Total Price"

    def cart_owner(self, obj):
        return obj.cart.customer_id.email

    cart_owner.short_description = "Cart Owner"


class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "order_owner")

    def order_number(self, obj):
        return obj.id

    order_number.short_description = "Order Number"

    def order_owner(self, obj):
        return obj.customer.email

    order_owner.short_description = "Order Owner"


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product_name", "quantity", "item_total_price", "order_owner")

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = "Product Name"

    def item_total_price(self, obj):
        return f"{site_currency_symbol}{obj.total_price}"

    item_total_price.short_description = "Total Price"

    def order_owner(self, obj):
        return obj.order.customer.email

    order_owner.short_description = "Order Owner"


admin.site.site_header = "Simple Store Admin"
admin.site.site_title = "Simple Store Admin"

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(
    [Category, Brand, Photo, Customer, Review, Rating,]
)

admin.site.unregister(Group)
