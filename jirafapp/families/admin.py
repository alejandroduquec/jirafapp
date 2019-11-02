"""Family models admin."""

# Django
from django.contrib import admin

# Models
from jirafapp.families.models import Kid, KidHeight


@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    """kid model admin."""
    
    list_display = ('name', 'gender', 'parent', 'birthdate')
    search_fields = ('parent', 'parent')


@admin.register(KidHeight)
class KidHeightAdmin(admin.ModelAdmin):
    """KidHeight model admin."""
    
    list_display = ('kid', 'height', 'date_height')
    search_fields = ('kid', )