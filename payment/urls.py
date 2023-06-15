from django.urls import path
from . import views


urlpatterns = [
    path("sucess/",views.PaymentSuccessView.as_view(),name="PaymentSuccessView"),
    path("razorpay-webhook/",views.RazorpayWebhook,name="RazorpayWebhook")
    ]
