from django.contrib import admin
from .models import Queue


@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    """Очередь"""
    list_display = ['created_at', 'contractor', 'own', 'status', 'expiration', 'trade_point']
    list_display_links = ['created_at', 'contractor', 'own', 'status', 'expiration', 'trade_point']

