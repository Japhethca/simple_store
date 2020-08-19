"""store app global context"""

from django.db.models import Sum

from simple_store.apps.core.models import Cart, CartItem


def cart(request):
    """Add global cart_items_number context"""
    cart_item_number = 0
    if request.user.is_authenticated:
        customer_cart, _ = Cart.objects.get_or_create(customer_id=request.user)
        cart_items = CartItem.objects.filter(cart=customer_cart).aggregate(
            Sum("quantity")
        )
        cart_item_number = cart_items.get("quantity__sum", 0)
    return {"cart_items_number": cart_item_number}
