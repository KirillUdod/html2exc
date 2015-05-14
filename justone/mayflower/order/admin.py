from django.contrib import admin

from order.models import Basket, Order

admin.site.register(Order)
admin.site.register(Basket)