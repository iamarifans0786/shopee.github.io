from django.urls import path
from accounts import views


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="LoginView"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.RegisterView.as_view(), name="RegisterView"),
    path("profile/", views.UserProfileView.as_view(), name="UserProfileView"),
    path("order/", views.OrderView.as_view(), name="OrderView"),
    path("order-detail/<int:order_id>", views.OrderDetailView.as_view(), name="OrderDetailView"),
    path("change-password/", views.change_password, name="change_password"),
]
