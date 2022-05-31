from django.contrib import admin
from .models import Employee


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Сотрудники"""
    list_display = ('name', 'surname', 'role', 'IIN', 'pdf',
                    'address', 'phone', 'birthdate', 'tradepoint')
    list_display_links = ('name',)
