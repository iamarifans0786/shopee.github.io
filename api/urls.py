from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', views.UserView)
router.register('product-categorie', views.ProductCategoryViewSets)
router.register('products', views.ProductViewSets)
# router.register('order', views.OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserAuthView.as_view()),
    path('carts/', views.CartView.as_view()),
    path('carts/<cartId>/', views.CartView.as_view()),
     path('wishlist/', views.WishlistView.as_view()),
    path('wishlist/<wishlistId>/', views.WishlistView.as_view()),
    path('carts-info/', views.AdditionalInfoCartView.as_view()),
    path('order/<orderId>/', views.OrderView.as_view()),
    path('order/', views.OrderView.as_view()),
]