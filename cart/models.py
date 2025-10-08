from django.db import models
from django.contrib.auth.models import User

from core.models import Product
# Create your models here.

class MyCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Cart ({self.user.username if self.user else "Guest"})"


class CartItem(models.Model):
    cart = models.ForeignKey(MyCart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ['cart', 'product']


    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity
    
