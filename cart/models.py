from django.db import models
from django.contrib.auth.models import User
from product.models import Product, ProductVariation,Brand


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    

    def __str__(self) -> str:
        return f"{self.product} {self.user.email}"

class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Wish List"
        verbose_name_plural = "Wish Lists"
    

    def __str__(self) -> str:
        return f"{self.product} {self.user.email}"