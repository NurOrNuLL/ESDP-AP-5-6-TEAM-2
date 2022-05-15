from django.contrib import admin
from .models import Nomenclature


# Register your models here.
@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    """Номенклатура"""
    list_display = ('name', 'organization')
