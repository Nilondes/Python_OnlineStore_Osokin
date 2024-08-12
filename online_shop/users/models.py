from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    pass


class ClientManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(username=user)


class CartManager(models.Manager):
    def order_for_user(self, user, order):
        return self.get_queryset().filter(username=user, order=order)


class OrderManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(username=user)


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
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
    username = models.ForeignKey(User, models.CASCADE)
    client_first_name = models.CharField(max_length=255)
    client_middle_name = models.CharField(max_length=255)
    client_last_name = models.CharField(max_length=255)
    client_address = models.CharField(max_length=255)
    client_email = models.EmailField(default='none')
    client_phone = models.CharField(max_length=255)
    objects = ClientManager()

    def __str__(self):
        return self.client_last_name

    def get_absolute_url(self):
        return reverse('base')


class Order(models.Model):
    order_status = models.CharField(max_length=255)
    username = models.ForeignKey(User, models.CASCADE, default=None)
    objects = OrderManager()

    def __str__(self):
        return str(self.pk)


class ProductAmount(models.Model):
    product = models.ForeignKey('Product', to_field='name', on_delete=models.CASCADE, default=None, unique=True)
    product_amount = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return str(self.product) + ', amount: ' + str(self.product_amount)


class Cart(models.Model):
    username = models.ForeignKey(User, models.CASCADE, default=None)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, default=None)
    objects = CartManager()

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('add_to_cart')
