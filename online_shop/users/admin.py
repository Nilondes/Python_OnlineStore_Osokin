from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, Category, Client, Order, ProductAmount, Cart


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(ProductAmount)
admin.site.register(Cart)
