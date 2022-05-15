from import_export import resources
from django.contrib import admin
from .models import Service
from import_export.admin import ImportExportModelAdmin


class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service


@admin.register(Service)
class ServiceAdmin(ImportExportModelAdmin):
    resource_class = ServiceResource
    list_display = ('id', 'category', 'name', 'price', 'note', 'price_category',)
