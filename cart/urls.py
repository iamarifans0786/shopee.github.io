from django.urls import path
from . import views


urlpatterns = [
    path("add-to-cart/", views.AddToCartView.as_view(), name="AddToCartView"),
    path("my-cart/", views.MyCartView.as_view(), name="MyCartView"),
    path(
        "remove-cart-item/<int:cart_id>",
        views.RemoveCartItem.as_view(),
        name="RemoveCartItem",
    ),
    path(
        "add-to-wishlist/<slug:product_slug>",
        views.AddToWishList.as_view(),
        name="AddToWishList",
    ),
    path("my-wishlist", views.MyWishListView.as_view(), name="MyWishListView"),
    path(
        "remove-wishlist-item/<int:wishlist_product_id>",
        views.RemoveWishListItem.as_view(),
        name="RemoveWishListItem",
    ),
    path("checkout", views.CheckoutView.as_view(), name="CheckoutView"),
    path("thank-you", views.ThankYouView.as_view(), name="ThankYouView"),
    path("error", views.ErrorPage.as_view(), name="ErrorPage"),
]
