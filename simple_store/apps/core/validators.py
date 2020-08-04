from django.core.exceptions import ValidationError
from django.utils.text import gettext_lazy as _


MAX_RATING = 10
MIN_RATING = 0


def is_valid_rating(value):
    if value > MAX_RATING or value < MIN_RATING:
        raise ValidationError(
            _(
                f"Rating must not be greater than {MAX_RATING} or less than {MIN_RATING}."
            )
        )
