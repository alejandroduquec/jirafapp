"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from jirafapp.users.models import (
    User,
    Province
)


class CustomUserAdmin(UserAdmin):
    """User model admin."""

    fieldsets = [
        [('Datos de usuario'), {
            'fields': ('first_name', 'code', 'password'),
        }],
        [('Datos de contacto'), {
            'fields': ('email', 'username'),
        }],
        [('Tipo usuario'), {
            'fields': ('is_active', 'is_superuser', 'is_staff'),
        }],
        [('Stats'), {
            'fields': ('created', 'modified', 'date_joined', 'last_login'),
        }],
    ]

    list_display = ('email', 'username', 'first_name', 'province', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'created')
    readonly_fields = ('created', 'modified', 'date_joined', 'last_login')


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    """Province model admin."""
    
    list_display = ('name', 'slug_name')
    search_fields = ('name', 'slug_name')


admin.site.register(User, CustomUserAdmin)
