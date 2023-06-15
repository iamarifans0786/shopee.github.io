from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Cart, WishList
from order.models import Order, OrderDetails
from product.models import Product
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import PlaceOrderForm
import razorpay
import datetime


@method_decorator(login_required, name="dispatch")
class AddToCartView(View):
    """Handle Post method for Add To Cart"""

    def get(self, request):
        return redirect("home_page")

    def post(self, request):
        quantity = request.POST.get("quantity")
        variation_id = request.POST.get("variation_id")
        product_id = request.POST.get("product_id")
        product = Product.objects.get(id=product_id)
        # try:
        #     cart = Cart.objects.get(user=request.user, product_id=product_id, variation_id=variation_id)
        #     cart.quantity = quantity
        #     cart.save()
        # except :
        #     cart = Cart.objects.create(
        #         quantity=quantity,
        #         variation_id=variation_id,
        #         product_id=product_id,
        #         user=request.user
        #     )
        cart, is_created = Cart.objects.get_or_create(
            user=request.user, product_id=product_id, variation_id=variation_id
        )
        cart.quantity = quantity
        cart.save()

        return redirect("MyCartView")


@method_decorator(login_required, name="dispatch")
class MyCartView(View):
    """For My Cart Page"""

    def get(self, request):
        cart_products = Cart.objects.prefetch_related("product").filter(
            user=request.user
        )
        sub_total = 0
        shipping = 50
        for cart_product in cart_products:
            cart_product.sub_total = cart_product.product.price * cart_product.quantity
            sub_total = sub_total + cart_product.sub_total
        if sub_total > 1000:
            shipping = 0
        grand_total = sub_total + shipping
        context = {
            "cart_products": cart_products,
            "sub_total": sub_total,
            "shipping": shipping,
            "grand_total": grand_total,
        }
        return render(request, "cart/my_cart.html", context)

    def post(self, request):
        return render(request, "cart/my_cart.html")


@method_decorator(login_required, name="dispatch")
class RemoveCartItem(View):
    """Delete an item from my cart"""

    def get(self, request, cart_id):
        try:
            Cart.objects.get(id=cart_id).delete()
        except:
            pass
        return redirect("MyCartView")


@method_decorator(login_required, name="dispatch")
class AddToWishList(View):
    """Handle Post method for Add To WishList"""

    def get(self, request, product_slug):
        product = Product.objects.get(slug=product_slug)
        print(product)
        wishlist = WishList.objects.create(user=request.user, product=product)
        wishlist.save()
        return redirect("home_page")


@method_decorator(login_required, name="dispatch")
class MyWishListView(View):
    """For My WishListView Page"""

    def get(self, request):
        wishlist_products = WishList.objects.select_related("product").filter(
            user=request.user
        )
        return render(
            request, "cart/my_wishlist.html", {"wishlist_products": wishlist_products}
        )


@method_decorator(login_required, name="dispatch")
class RemoveWishListItem(View):
    """Delete an item from my cart"""

    def get(self, request, wishlist_product_id):
        try:
            WishList.objects.get(id=wishlist_product_id).delete()
        except:
            pass
        return redirect("MyWishListView")


class ThankYouView(View):
    """Thank you page for redirect success"""

    def get(self, request):
        return render(request, "thank-you.html")


class ErrorPage(View):
    """Page Not Found page for redirect any error occur"""

    def get(self, request):
        return render(request, "404.html")


@method_decorator(login_required, name="dispatch")
class CheckoutView(View):
    """Process for Checkout And Order"""

    form_class = PlaceOrderForm
    template_name = "cart/checkout.html"

    def get(self, request):
        initial = {
            "address": request.user.user_profile.address,
            "mobile": request.user.user_profile.mobile,
        }
        cart_products = Cart.objects.filter(user=request.user)
        user_detail = User.objects.get(id=request.user.id)
        form = self.form_class(initial=initial)
        sub_total = 0
        shipping = 50
        for cart_product in cart_products:
            cart_product.sub_total = cart_product.product.price * cart_product.quantity
            sub_total = sub_total + cart_product.sub_total
        if sub_total > 1000:
            shipping = 0
        grand_total = sub_total + shipping
        context = {
            "form": form,
            "sub_total": sub_total,
            "shipping": shipping,
            "grand_total": grand_total,
            "user_detail": user_detail,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        cart_products = Cart.objects.filter(user=request.user)
        sub_total = 0
        shipping = 50
        for cart_product in cart_products:
            cart_product.sub_total = cart_product.product.price * cart_product.quantity
            sub_total = sub_total + cart_product.sub_total
        if sub_total > 1000:
            shipping = 0
        grand_total = int((sub_total + shipping) * 100)

        client = razorpay.Client(
            auth=("rzp_test_GtCud6v3BP5VGm", "0VzfjHQNclSACQoJXwrLF9vK")
        )
        receipt = f"order_rcptid{request.user.id}"
        data = {"amount": grand_total, "currency": "INR", "receipt": receipt}
        payment = client.order.create(data=data)
        if payment.get("id"):
            context = {
                "order_id": payment["id"],
                "amount": payment["amount"],
                "first_name": first_name,
                "last_name": last_name,
                "address": request.POST.get("address"),
                "mobile": request.POST.get("mobile"),
            }
            return render(request, "cart/capture-payment.html", context)
        return JsonResponse({"message": "Error"})
