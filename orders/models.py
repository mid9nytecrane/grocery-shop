from django.db import models
from django.contrib.auth.models import User 
from core.models import Product 

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('On Delivery', 'On Delivery'),
        ('Delivered', 'Delivered')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    full_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200,null=True)
    town = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    momo_reference = models.CharField(max_length=255, null=True , blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
