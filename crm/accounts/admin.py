from django.contrib import admin
from .models import Customer, Product, Order, Tag, OrderItem

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)
admin.site.register(OrderItem)