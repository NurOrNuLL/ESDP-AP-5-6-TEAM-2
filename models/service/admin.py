from import_export import resources
from import_export.fields import Field
from django.contrib import admin
from .models import Service
from ..nomenclature.models import Nomenclature
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget


class ServiceResource(resources.ModelResource):
    """Для импорта и экспорта данных услуг"""
    nomenclature = Field(
        attribute='nomenclature', column_name='Номенклатура',
        saves_null_values=False,
        widget=ForeignKeyWidget(Nomenclature, field='name')
    )
    name = Field(attribute='name', column_name='Название', saves_null_values=False)
    category = Field(attribute='category', column_name='Категория', saves_null_values=False)
    mark = Field(attribute='mark', column_name='Марка', saves_null_values=False)
    note = Field(attribute='note', column_name='Примечание', saves_null_values=True)
    price = Field(attribute='price', column_name='Цена', saves_null_values=False)

    class Meta:
        model = Service


@admin.register(Service)
class ServiceAdmin(ImportExportModelAdmin):
    """Услуги"""
    resource_class = ServiceResource
    list_display = ('id', 'nomenclature', 'name', 'category',
                    'mark', 'note', 'price')
    list_display_links = ('id', 'name')
