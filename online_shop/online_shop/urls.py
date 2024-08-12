"""
URL configuration for online_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from online_shop import settings
from users.views import (product_list,
                         product_detail,
                         register,
                         ClientCreateView,
                         ClientListView,
                         add_to_cart,
                         orders,
                         order_detail,
                         submit_order,
                         remove_cart)
from django.contrib.auth import views as auth_views
from django.shortcuts import render


def home_view(request):
    return render(request, 'base.html')


urlpatterns = [
    path('', home_view, name='base'),
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('orders/', orders, name='orders'),
    path('orders/<int:pk>', order_detail, name='order_detail'),
    path('orders/<int:pk>/<int:pk1>', remove_cart, name='remove_cart'),
    path('orders/<int:pk>/submit', submit_order, name='submit_order'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('cabinet/', ClientListView.as_view(template_name='cabinet.html'), name='cabinet'),
    path('cabinet/create_client/', ClientCreateView.as_view(template_name='create_client.html'), name='create_client'),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)