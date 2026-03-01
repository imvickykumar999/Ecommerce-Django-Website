from django.contrib import admin
from .models import Customer, Category, Order, Product

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
