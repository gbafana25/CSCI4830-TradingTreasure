from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

# Create your models here.

class Address(models.Model):
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.IntegerField()

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state} {self.zip_code}"


class User(AbstractUser):  # Extending Django's built-in user model
    location = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.BigIntegerField(blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    
    list_display = ("id", "username", "email", "location", "phone_number")
    fieldsets = [
        (None, {"fields": ["id", "username", "email", "location", "phone_number"]}),
        ("Personal info", {"fields": ["id", "username", "email", "location", "phone_number"]})
    ]

    def __str__(self):
        if self.location == None or self.phone_number == None:
            return self.username
        return f"{self.username}, {self.email}, {self.location}, {str(self.phone_number)}\n{self.address}"

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    category = models.TextField()  # Store categories as semicolon-separated values
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    date_posted = models.DateTimeField(auto_now_add=True)
    buyer_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    is_bought = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image:
            return self.image.url
        return '/productionfiles/images/placeholder.jpg'


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    buyer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    seller = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sales', null=True, blank=True)
    buyer_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order for {self.product.name} by {self.buyer.username}"
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    time_ordered = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders_bought")
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders_sold")
    buyer_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.name}"