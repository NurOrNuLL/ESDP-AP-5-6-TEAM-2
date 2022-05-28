from django.contrib import admin
from .models import Employee


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Сотрудники"""
    list_display = ('id', 'name', 'surname', 'role', 'IIN', 'pdf',
                    'address', 'phone', 'birthdate', 'tradepoints')
    list_display_links = ('id', 'name',)
