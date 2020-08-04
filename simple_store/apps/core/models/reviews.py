from django.db import models


from ..validators import is_valid_rating


class Review(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    review = models.TextField()
    customer_id = models.ForeignKey("User", on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review


class Rating(models.Model):
    stars = models.SmallIntegerField(validators=[is_valid_rating])

    def __str__(self):
        return self.stars
