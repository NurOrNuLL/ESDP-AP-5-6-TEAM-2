from django.contrib import admin
from .models import Organization


# Register your models here.
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Организация"""
    list_display = ('id', 'name', 'address', 'RNN', 'BIN', 'bank_requisition',)
    list_display_links = ('id', 'name', )
