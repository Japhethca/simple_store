from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

PENDING = "PENDING"
COMPLETED = "COMPLETED"
CANCELLED = "CANCELLED"

ORDER_STATUSES = (
    (PENDING, PENDING),
    (COMPLETED, COMPLETED),
    (CANCELLED, CANCELLED),
)

User = get_user_model()


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUSES, default=PENDING)
    date_placed = models.DateTimeField()

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
