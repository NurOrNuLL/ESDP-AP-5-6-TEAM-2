from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


# Register your models here.
@admin.register(get_user_model())
class UserAdmin(UserAdmin):
    """Пользователь"""
    list_display = ['username', 'first_name', 'last_name', 'is_staff', 'is_superuser',
                    'is_active']
    list_display_links = ('username',)
