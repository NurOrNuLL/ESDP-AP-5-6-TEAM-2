from django.contrib import admin
from .models import Queue


@admin.register(Queue)
class Queue(admin.ModelAdmin):
    list_display = ['created_at', 'contractor', 'own', 'status', 'expiration']
    list_display_links = ['created_at', 'contractor', 'own', 'status', 'expiration']
