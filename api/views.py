from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import viewsets, views, response, filters, authentication, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import F, Sum
from django.contrib.auth.models import User
from product.models import ProductCategory, Product
from cart.models import Cart, WishList
from order.models import Order,OrderDetails
from . import serializers


class UserAuthView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserView(viewsets.ModelViewSet):
    """User CRUD Operation"""

    serializer_class = serializers.UserAuthSerializer
    queryset = User.objects.filter(is_superuser=False, is_staff=False)


class ProductCategoryViewSets(viewsets.ModelViewSet):
    """Product Category API"""

    serializer_class = serializers.ProductCategorySerializer
    queryset = ProductCategory.objects.filter(status=True)
    http_method_names = ["get"]


class ProductViewSets(viewsets.ModelViewSet):
    """Product API"""

    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.filter(status=True)
    http_method_names = ["get"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["product_category__slug"]
    ordering_fields = ["price"]


class AdditionalInfoCartView(views.APIView):
    """Additional info about current users cart"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shipping = 50
        discount = 0
        cart_products = Cart.objects.filter(user=request.user).annotate(
            sub_total=F("product__price") * F("quantity")
        )
        sub_total = cart_products.aggregate(total=Sum("sub_total"))["total"]
        grand_total = sub_total + shipping
        return response.Response(
            {
                "shipping": shipping,
                "discount": discount,
                "sub_total": sub_total,
                "grand_total": grand_total,
            }
        )


class CartView(views.APIView):
    """Cart API View"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def get(self, request, cartId=None):
        """Get all cart items for current user"""
        # queryset = Cart.objects.filter(user=request.user)
        cart_products = Cart.objects.filter(user=request.user).annotate(
            sub_total=F("product__price") * F("quantity")
        )  # Calculate Product Subtotal
        serializer = self.serializer_class(cart_products, many=True)
        return response.Response(serializer.data)

    def post(self, request, cartId=None):
        """Add to cart"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data.get("quantity")
            product = serializer.validated_data.get("product")
            variation = serializer.validated_data.get("variation")
            cart, is_created = Cart.objects.get_or_create(
                user=request.user, product=product, variation=variation
            )
            """get_or_create() : create cart or which is alredy created cart it will only get"""
            cart.quantity = quantity
            cart.save()
            return response.Response({"status": "Success"}, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cartId=None):
        try:
            Cart.objects.get(id=cartId).delete()
            return response.Response({"status": "success"})
        except Cart.DoesNotExist:
            return response.Response(
                {"details": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )


class WishlistView(views.APIView):
    """Cart API View"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WishlistSerializer

    def get(self, request, wishlistId=None):
        """Get all wishlist items for current user"""

        wishlist_products = WishList.objects.filter(user=request.user)
        serializer = self.serializer_class(wishlist_products, many=True)
        return response.Response(serializer.data)

    def post(self, request, wishlistId=None):
        """Add to wishlist"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data.get("product")
            wishlist, is_created = WishList.objects.get_or_create(
                user=request.user, product=product
            )
            wishlist.save()
            return response.Response({"status": "Success"}, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, wishlistId=None):
        try:
            WishList.objects.get(id=wishlistId).delete()
            return response.Response({"status": "success"})
        except WishList.DoesNotExist:
            return response.Response(
                {"details": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )


class OrderView(views.APIView):
    """Cart API View"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.OrderSerializer

    def get(self, request, orderId=None):
        """Get all order items for current user"""
        orders = Order.objects.filter(user=request.user)
        serializer = self.serializer_class(orders, many=True)
        return response.Response(serializer.data)

    def post(self, request, orderId=None):
        """Order Placed"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data.get("user_name")
            address = serializer.validated_data.get("address")
            mobile = serializer.validated_data.get("mobile")
            order_status = serializer.validated_data.get("order_status")
            payment_status = serializer.validated_data.get("payment_status")
            razor_pay_order_id = serializer.validated_data.get("razor_pay_order_id")
            
            price = serializer.validated_data.get('order_detail["price"]')
            product = serializer.validated_data.get('order_detail["product"]')
            quantity = serializer.validated_data.get('order_detail["quantity"]')
            variation = serializer.validated_data.get('order_detail["variation"]')

            order, is_created = Order.objects.get_or_create(
                user=request.user,
                user_name=user_name,
                address=address,
                mobile=mobile,
                order_status=order_status,
                payment_status=payment_status,
                razor_pay_order_id=razor_pay_order_id,
            )
            order.save()
            order_detail, is_created = OrderDetails.objects.get_or_create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
                variation=variation,
            )
            order_detail.save()
            
            return response.Response({"status": "Success"}, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
