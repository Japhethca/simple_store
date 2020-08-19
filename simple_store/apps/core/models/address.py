from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BillingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.postal_code}, {self.country}"

    class Meta:
        ordering = ["first_name"]

    @classmethod
    def set_as_default(cls, obj):
        cls.objects.filter(customer=obj.customer).update(is_default=False)
        obj.is_default = True
        obj.save()
