from django.contrib import admin
from .models import Brand, Product, Order, ProductOrder

# Register your models here.
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ProductOrder)