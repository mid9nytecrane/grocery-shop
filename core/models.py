from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify 


# Create your models here.

class Profile(models.Model):
    GENDER = {
        "male":"MALE",
        "female":"FEMALE",
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, null=True)
    address = models.CharField(max_length=50, null=True)
    region = models.CharField(max_length=100, null=True)
    town = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=8, choices=GENDER, default="")
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.user}'s profile"


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.name 


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.slug:   
            self.slug = slugify(self.name)
        super(Category, self).save()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name 
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(null=True, upload_to='images/', blank=True)
    is_sold = models.BooleanField(default=False)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name="products" )
    is_added_to_cart = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    adddress = models.CharField(max_length=250, default="", null=True , blank=True)
    phone = models.CharField(max_length=15, default='', blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"order - {self.id} ({self.product})"
    


