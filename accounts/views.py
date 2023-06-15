from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from order.models import Order, OrderDetails
from django.views import View
from accounts.forms import (
    UserAuthenticationForm,
    CustomUserCreationForm,
    CustomChangePasswordForm,
    UserForm,
    UserProfileForm,
)
from django.contrib.auth import login, logout


class LoginView(View):
    """Login Logout View"""

    form_class = UserAuthenticationForm
    template_name = "account/login.html"

    def get(self, request):
        redirect_url = request.GET.get("next")
        form = self.form_class(initial={"redirect_url": redirect_url})
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            redirect_url = form.cleaned_data.get("redirect_url")
            if redirect_url:
                return redirect(redirect_url)
            return redirect("home_page")
        context = {"form": form}
        return render(request, self.template_name, context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("home_page")


class RegisterView(View):
    form_class = CustomUserCreationForm
    template_name = "account/register.html"

    def get(self, request):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            print("User Created Successfull...")
            return redirect("LoginView")
        context = {"form": form}
        print("Something Wrong...")
        return render(request, self.template_name, context)


@method_decorator(login_required, name="dispatch")
class UserProfileView(View):
    """User Prifile View For Update profile Details and change password"""

    form_class = UserForm
    profile_form_class = UserProfileForm
    change_password_form_class = CustomChangePasswordForm
    template_name = "account/profile.html"

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        profile_details = UserProfile.objects.get(user=request.user)
        user_form = self.form_class(instance=user)
        user_profile_form = self.profile_form_class(instance=user.user_profile)
        change_password_form = self.change_password_form_class(user)
        context = {
            "user_form": user_form,
            "user_profile_form": user_profile_form,
            "profile_pic": profile_details.profile_image,
            "change_password_form": change_password_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        user_form = self.form_class(request.POST, instance=user)
        user_profile_form = self.profile_form_class(
            request.POST, request.FILES, instance=user.user_profile
        )
        change_password_form = self.change_password_form_class(
            request.user, request.POST
        )
        """profile updation"""
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return redirect("UserProfileView")
        """Change Password"""
        if change_password_form.is_valid():
            change_password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("home_page")
        context = {
            "user_form": user_form,
            "user_profile_form": user_profile_form,
            "change_password_form": change_password_form,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name="dispatch")
class OrderView(View):
    """class for view order status"""

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return render(request, "account/order-history.html", {"orders": orders})


@method_decorator(login_required, name="dispatch")
class OrderDetailView(View):
    """class for complate detail of order products"""

    def get(self, request, order_id):
        order_details = (
            OrderDetails.objects.prefetch_related("product")
            .select_related("order")
            .filter(order_id=order_id)
        )
        return render(
            request,
            "account/order-history-products.html",
            {"order_details": order_details},
        )


def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        conform_password = request.POST.get("confrom_password")
        print(old_password)
        print(new_password, conform_password)

    return render(request, "account/profile.html")
