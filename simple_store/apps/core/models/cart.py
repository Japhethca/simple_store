from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(models.Model):
    customer_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"customer: {self.customer_id.username}"


class CartItem(models.Model):
    product_id = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Product name: {self.product_id.name}, total price: {self.total_price}, quantity: {self.quantity}"
