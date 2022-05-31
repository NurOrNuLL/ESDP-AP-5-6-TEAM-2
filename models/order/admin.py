from django.contrib import admin
from .models import Order


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Заказ-наряд"""
    list_display = ('id', 'created_at', 'contractor', 'price', 'status')
    list_display_links = ('id', 'created_at', 'contractor', 'price', 'status')
