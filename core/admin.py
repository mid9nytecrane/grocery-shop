from django.contrib import admin

# Register your models here.

from core.models import Customer, Product, Category, Order,Profile

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Profile)