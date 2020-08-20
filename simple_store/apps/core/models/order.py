from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

ORDER_PENDING = "PENDING"
ORDER_COMPLETED = "COMPLETED"
ORDER_CANCELLED = "CANCELLED"
ORDER_AWAITING_PAYMENT = "AWAITING PAYMENT"

ORDER_STATUSES = (
    (ORDER_PENDING, ORDER_PENDING),
    (ORDER_COMPLETED, ORDER_COMPLETED),
    (ORDER_CANCELLED, ORDER_CANCELLED),
    (ORDER_AWAITING_PAYMENT, ORDER_AWAITING_PAYMENT),
)

PAYMENT_METHOD_CARD = "card"
PAYMENT_METHOD_BANK = "bank"
PAYMENT_METHODS = (
    (PAYMENT_METHOD_BANK, PAYMENT_METHOD_BANK),
    (PAYMENT_METHOD_CARD, PAYMENT_METHOD_CARD),
)
User = get_user_model()


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=ORDER_STATUSES, default=ORDER_AWAITING_PAYMENT
    )
    date_placed = models.DateTimeField()
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHODS, default=PAYMENT_METHOD_CARD
    )

    class Meta:
        ordering = ["-date_placed"]

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_placed = timezone.now()
        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"order_number: {self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.name
