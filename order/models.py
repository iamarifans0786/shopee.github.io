from django.db import models
from django.contrib.auth.models import User
from product.models import Product, ProductVariation


class Order(models.Model):
    ORDER_STATUS = (
        ("Pending", "Pending"),
        ("In-progress", "In-progress"),
        ("Delivered", "Delivered"),
        ("canceled", "canceled"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    user_name = models.CharField(max_length=255)
    address = models.TextField()
    mobile = models.CharField(max_length=13, null=True)
    order_status = models.CharField(
        choices=ORDER_STATUS, max_length=255, default="Pending"
    )
    payment_status = models.BooleanField(default=False)
    razor_pay_order_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{str(self.id)} {self.user}"


class OrderDetails(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_detail"
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    variation = models.ForeignKey(
        ProductVariation, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{str(self.order.id)} {self.product}"

    class Meta:
        verbose_name = "Order Detail"
