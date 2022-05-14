from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Услуги"""
    list_display = ('category', 'name', 'price', 'note', 'price_category',)
