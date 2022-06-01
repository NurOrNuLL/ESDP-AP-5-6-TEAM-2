from django.contrib import admin
from .models import Contractor


# Register your models here.
@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    """Контрагент"""
    list_display = ('id', 'name', 'address', 'IIN_or_BIN', 'IIC', 'bank_name',
                    'BIC', 'phone', 'trust_person', 'organization')
    list_display_links = ('id', 'name',)
