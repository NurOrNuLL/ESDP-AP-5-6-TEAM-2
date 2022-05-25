from django.contrib import admin
from .models import Own


@admin.register(Own)
class OwnAdmin(admin.ModelAdmin):
    """Собственность"""
    list_display = ('id', 'name', 'contractor', 'number', )
    list_display_links = ('id', 'name', 'contractor', )
    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
        (None, {
            'fields': ('contractor', )
        }),
        (None, {
            'fields': ('number', )
        }),
    )
