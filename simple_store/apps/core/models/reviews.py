from django.db import models
from django.contrib.auth.models import User

from ..validators import is_valid_rating
from .customers import Customer


class Review(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    review = models.TextField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review


class Rating(models.Model):
    stars = models.SmallIntegerField(validators=[is_valid_rating])
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.stars}"
