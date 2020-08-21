from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=500, unique=True, db_index=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    description = models.TextField()
    categories = models.ForeignKey("Category", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", null=True, blank=True, on_delete=models.SET_NULL)
    discounts = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True
    )
    color = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ("name",)

    def clean(self):
        if self.price <= 0:
            raise ValidationError({"price": _("price cannot be less than 0.")})

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "Category", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Catogories"


class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    logo = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    upload = models.FileField(upload_to="images")
    is_cover = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.upload.url
