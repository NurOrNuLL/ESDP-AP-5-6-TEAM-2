from django.contrib import admin
from .models import PaymentMethod


# Register your models here.
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    """Способ оплаты"""
    list_display = ('id', 'name')
    list_display_links = ('id', 'name',)
