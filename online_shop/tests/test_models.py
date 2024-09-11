from django.test import TestCase
from users.models import Product, Client, Cart, Category, User, Order, ProductAmount

class CreateClient(TestCase):
    def test_client_creation(self):
        user = User.objects.create(username='test_user')
        client = Client.objects.create(username=user,
                                       client_first_name='test_name',
                                       client_last_name='test_last_name',
                                       client_middle_name='test_middle_name',
                                       client_address='12345 New York',
                                       client_email='test@example.com',
                                       client_phone='123456789')
        self.assertEqual(client.username, user)


class CreateProduct(TestCase):
    def test_product_creation(self):
        category = Category.objects.create(name='test')
        product = Product.objects.create(name='Test Product',
                                         description='test_description',
                                         price=10,
                                         image='path',
                                         category=category)
        self.assertEqual(product.name, 'Test Product')
        add_product_to_storage = ProductAmount.objects.create(product=product,
                                                   product_amount=100)
        self.assertEqual(add_product_to_storage.product_amount, 100)


class CreateOrder(TestCase):
    def test_order_creation(self):
        user = User.objects.create(username='test_user')
        order = Order.objects.create(username=user,
                                     order_status='new'
                                     )
        self.assertEqual(order.order_status, 'new')
        category = Category.objects.create(name='test')
        product = Product.objects.create(name='Test Product',
                                         description='test_description',
                                         price=10,
                                         image='path',
                                         category=category)
        cart = Cart.objects.create(username=user,
                                   product=product,
                                   quantity=10,
                                   order=order)
        self.assertEqual(cart.quantity, 10)
