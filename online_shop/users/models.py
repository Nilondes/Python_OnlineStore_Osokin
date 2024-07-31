from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Client(models.Model):
    client_first_name = models.CharField(max_length=255)
    client_middle_name = models.CharField(max_length=255)
    client_last_name = models.CharField(max_length=255)
    client_address = models.CharField(max_length=255)
    client_email = models.CharField(max_length=255)
    client_phone = models.CharField(max_length=255)

    def __str__(self):
        return self.client_last_name


class Order(models.Model):
    order_status = models.CharField(max_length=255)

    def __str__(self):
        return str(self.pk)


class ProductAmount(models.Model):
    item_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    item_amount = models.IntegerField()

    def __str__(self):
        return self.item_id


class Basket(models.Model):
    order_id = models.ForeignKey('Order', on_delete=models.PROTECT)
    item_id = models.ForeignKey('Product', on_delete=models.PROTECT)
    client_id = models.ForeignKey('Client', on_delete=models.PROTECT)
    item_amount = models.IntegerField()

    def __str__(self):
        return self.order_id
