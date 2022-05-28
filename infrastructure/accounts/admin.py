from django.contrib import admin
from django.contrib.auth import get_user_model


# Register your models here.
@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    """Пользователь"""
    list_display = ['id', 'username', 'first_name', 'last_name', 'is_staff', 'is_superuser',
                    'is_active']
    list_display_links = ('id', 'username',)
