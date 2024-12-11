from django.contrib import admin
from .models import order,OrderItem

# Register your models here.
admin.site.register(order)

class OrderItemAdmin(admin.ModelAdmin):
    list_display=["order","products","quantity"]
    #orderitem varibales
admin.site.register(OrderItem,OrderItemAdmin)