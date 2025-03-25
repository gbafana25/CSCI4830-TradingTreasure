from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Order, Address, Product

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Product)