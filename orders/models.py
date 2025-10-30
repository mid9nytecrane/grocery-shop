from django.db import models
from django.contrib.auth.models import User 
from core.models import Product 

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('On Delivery', 'On Delivery'),
        ('Delivered', 'Delivered')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=200, null=True)
    order_number = models.CharField(max_length=50, unique=True,null=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200,null=True)
    town = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    paystack_reference = models.CharField(max_length=255, null=True , blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"
    
    @property
    def order_id(self):
        return f"#{self.id}"

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self) -> float:
        return self.quantity * self.price
