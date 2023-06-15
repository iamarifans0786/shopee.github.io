from cart.models import WishList


def wishlist_count_config(request):
    """Context processor for dynamic Cart Count"""
    wishlists = []
    wishlist_count=0
    if request.user.is_authenticated:
        wishlist_products = WishList.objects.filter(user=request.user)
        for wishlist_product in wishlist_products:
            wishlists.append(wishlist_product)
        wishlist_count = len(wishlists)
    return {"wishlist_count": wishlist_count}
