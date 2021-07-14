from django.contrib import admin
from .models import Product, Customer, Cart, OrederPlaced


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'selling_price', 'discount_price', 'description', 'brand', 'category', 'image']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'locality', 'city', 'zipcode', 'state']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user',  'product', 'quantity']


@admin.register(OrederPlaced)
class OrderAdmin(admin.ModelAdmin):
    list_display = [ 'product', 'customer', 'quantity', 'status', 'ordered_date']
