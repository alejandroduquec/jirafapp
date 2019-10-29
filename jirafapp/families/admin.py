"""Family models admin."""

# Django
from django.contrib import admin

# Models
from jirafapp.families.models import Kid


@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    """kid model admin."""
    
    list_display = ('name', 'gender', 'parent', 'birthdate')
    search_fields = ('parent', 'parent')