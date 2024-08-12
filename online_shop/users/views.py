from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Product, Cart, User, Client, Order, ProductAmount
from .forms import CartForm
from django.contrib.auth.forms import BaseUserCreationForm, UsernameField
from django.contrib.auth import login
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ClientListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")
    template_name = "cabinet.html"

    def get_queryset(self):
        return Client.objects.for_user(self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['client_first_name',
              'client_middle_name',
              'client_last_name',
              'client_address',
              'client_email',
              'client_phone']

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}


def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    return render(request, 'product_detail.html', context)


def add_to_cart(request):
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            order, create = Order.objects.get_or_create(username=request.user, order_status='new')
            cart, create = Cart.objects.get_or_create(username=request.user, product=product, order=order)
            Cart.objects.get_queryset().filter(id=cart.id).update(quantity=cart.quantity + quantity)
            return redirect('add_to_cart')
        else:
            form = CartForm()
    else:
        form = CartForm()
    return render(request, 'add_to_cart.html', {'form': form})


def remove_cart(request, pk, pk1):
    cart = Cart.objects.get_queryset().filter(id=pk1)
    cart.delete()
    return redirect('order_detail', pk)


def orders(request):
    user_orders = Order.objects.for_user(request.user)
    context = {'orders': user_orders}
    return render(request, 'orders.html', context)


def order_detail(request, pk):
    carts = Cart.objects.order_for_user(request.user, pk)
    order = Order.objects.get(pk=pk)
    context = {'carts': carts, 'order': order, 'status': 0}
    return render(request, 'order_detail.html', context)


def submit_order(request, pk):
    carts = Cart.objects.order_for_user(request.user, pk)
    transactions = {}
    order = Order.objects.get(pk=pk)

    for cart in carts:
        product_amount = ProductAmount.objects.get(product=cart.product)
        if product_amount.product_amount >= cart.quantity:
            transactions.update({cart.product: [product_amount.product_amount, cart.quantity]})
        else:
            context = {'carts': carts,
                       'order': order,
                       'status': 1,
                       'product': cart.product,
                       'amount': product_amount.product_amount
                       }
            return render(request, 'order_detail.html', context)

    for product, transaction in transactions.items():
        ProductAmount.objects.get_queryset().filter(product=product).update(
            product_amount=transaction[0] - transaction[1]
        )
    Order.objects.get_queryset().filter(id=pk).update(order_status='submitted')
    return redirect('orders')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('base')
        else:
            form = UserCreationForm()
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
