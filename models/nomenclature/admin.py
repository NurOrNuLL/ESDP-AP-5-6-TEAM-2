from django.contrib import admin
from .models import Nomenclature


# Register your models here.
@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    """Номенклатура"""
    list_display = ('id', 'name', 'organization')
    list_display_links = ('id', 'name',)
    fieldsets = (
        (None, {
            "fields": ("name",)
        }),
        (None, {
            "fields": ("organization", )
        }),
        (None, {
            "fields": ("services", )
        })
    )


admin.site.site_title = "Django ESDP-AP-5-6-TEAM-2"
admin.site.site_header = "Django ESDP-AP-5-6-TEAM-2"
