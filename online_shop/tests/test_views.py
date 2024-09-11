from django.test import TestCase
from users.models import Product, Client, Cart, Category, User, Order, ProductAmount
from users.views import add_to_cart, product_list, product_detail, remove_cart, orders, order_detail, submit_order
from django.urls import reverse
from django.test.client import RequestFactory


class ProductsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    def test_products_list(self):
        category = Category.objects.create(name='test')
        product_1 = Product.objects.create(name='First Product',
                                         description='test_description',
                                         price=10,
                                         image='path',
                                         category=category)
        product_2 = Product.objects.create(name='Second Product',
                                           description='test_description',
                                           price=15,
                                           image='path',
                                           category=category)
        req = self.factory.get(reverse('product_list'))
        resp = product_list(req)
        self.assertEqual(resp.status_code, 200)


class ProductTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    def test_product_detail(self):
        category = Category.objects.create(name='test')
        product = Product.objects.create(name='First Product',
                                         description='test_description',
                                         price=10,
                                         image='path',
                                         category=category)
        req = self.factory.get(reverse('product_detail', kwargs={'pk': product.pk}))
        resp = product_detail(req, product.pk)
        self.assertEqual(resp.status_code, 200)


class AddToCartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    def test_add_to_cart(self):
        category = Category.objects.create(name='test')
        product = Product.objects.create(name='Test Product',
                                         description='test_description',
                                         price=10,
                                         image='path',
                                         category=category)
        user = User.objects.create(username='test_user')
        client = Client.objects.create(username=user,
                                       client_first_name='test_name',
                                       client_last_name='test_last_name',
                                       client_middle_name='test_middle_name',
                                       client_address='12345 New York',
                                       client_email='test@example.com',
                                       client_phone='123456789')
        req = self.factory.post(reverse('add_to_cart'), {'quantity': 10, 'product':product.pk})
        req.user = user
        add_to_cart(req)
        cart = Cart.objects.get_queryset().filter(username=user)[0]
        self.assertEqual(cart.quantity, 10)
        add_to_cart(req)
        cart = Cart.objects.get_queryset().filter(username=user)[0]
        self.assertEqual(cart.quantity, 20)


class RemoveCartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    def test_cart_removal(self):
        user = User.objects.create(username='test_user')
        order = Order.objects.create(username=user,
                                     order_status='new'
                                     )
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
        req = self.factory.get(reverse('remove_cart', kwargs={'pk': order.pk, 'pk1': cart.pk}))
        resp = remove_cart(req, order.pk, cart.pk)
        with self.assertRaises(Exception):
            Cart.objects.get(pk=cart.pk)


class OrdersTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    def test_orders_list(self):
        user = User.objects.create(username='test_user')
        order = Order.objects.create(username=user,
                                     order_status='new'
                                     )
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
        req = self.factory.get(reverse('orders'))
        req.user = user
        resp = orders(req)
        self.assertEqual(resp.status_code, 200)


class OrderTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    def test_order_detail(self):
        user = User.objects.create(username='test_user')
        order = Order.objects.create(username=user,
                                     order_status='new'
                                     )
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
        req = self.factory.get(reverse('order_detail', kwargs={'pk': order.pk}))
        req.user = user
        resp = order_detail(req, order.pk)
        self.assertEqual(resp.status_code, 200)


class SubmitOrderTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    def test_order_submission(self):
        user = User.objects.create(username='test_user')
        order = Order.objects.create(username=user,
                                     order_status='new'
                                     )
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
        add_product_to_storage = ProductAmount.objects.create(product=product,
                                                   product_amount=12)
        req = self.factory.get(reverse('submit_order', kwargs={'pk': order.pk}))
        req.user = user
        resp = submit_order(req, order.pk)
        submitted_order = Order.objects.get(pk=order.pk)
        self.assertEqual(submitted_order.order_status, 'submitted')
        product_amount = ProductAmount.objects.get(product=product)
        self.assertEqual(product_amount.product_amount, add_product_to_storage.product_amount - cart.quantity)
    def test_failed_order_submission(self):
        user = User.objects.create(username='test_user')
        order = Order.objects.create(username=user,
                                     order_status='new'
                                     )
        category = Category.objects.create(name='test')
        product = Product.objects.create(name='Test Product',
                                         description='test_description',
                                         price=10,
                                         image='path',
                                         category=category)
        cart = Cart.objects.create(username=user,
                                   product=product,
                                   quantity=15,
                                   order=order)
        add_product_to_storage = ProductAmount.objects.create(product=product,
                                                              product_amount=12)
        req = self.factory.get(reverse('submit_order', kwargs={'pk': order.pk}))
        req.user = user
        resp = submit_order(req, order.pk)
        submitted_order = Order.objects.get(pk=order.pk)
        self.assertEqual(submitted_order.order_status, 'new')
        product_amount = ProductAmount.objects.get(product=product)
        self.assertEqual(product_amount.product_amount, add_product_to_storage.product_amount)
