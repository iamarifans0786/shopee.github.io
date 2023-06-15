from cart.models import Cart


def cart_count_config(request):
    """Context processor for dynamic Cart Count"""
    cart_count = 0
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        for cart in carts:
            cart_count = cart_count + cart.quantity
    return {"cart_count": cart_count}
