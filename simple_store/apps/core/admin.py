from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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


admin.site.register(User, UserAdmin)
admin.site.register(
    [
        Product,
        Category,
        Brand,
        Photo,
        Customer,
        Review,
        Rating,
        Cart,
        CartItem,
        Order,
        OrderItem,
    ]
)

admin.site.unregister(Group)
