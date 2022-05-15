from django.contrib import admin
from .models import TradePoint


@admin.register(TradePoint)
class TradePointAdmin(admin.ModelAdmin):
    """Торговая точка"""
    list_display = ('name', 'address', 'organization', 'nomenclature')
