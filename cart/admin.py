from django.contrib import admin
from .models import MyCart, CartItem
# Register your models here.

admin.site.register(MyCart)
admin.site.register(CartItem)