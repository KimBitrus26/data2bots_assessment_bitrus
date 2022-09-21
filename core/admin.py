from django.contrib import admin
from .models import (Category, Order, Price, Product, )

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Price)
admin.site.register(Product)
