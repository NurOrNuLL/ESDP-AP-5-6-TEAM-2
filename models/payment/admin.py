from django.contrib import admin
from .models import Payment


# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Оплата"""
    list_display = ('id', 'payment_status', 'method', 'details')
    list_display_links = ('id', 'payment_status', 'method', 'details')
