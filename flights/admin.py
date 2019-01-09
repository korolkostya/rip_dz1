from django.contrib import admin
from .models import Flight


@admin.register(Flight)
class ServiceAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)
    prepopulated_fields = {'slug': ('flightnumb',)}
    list_filter = ('active', 'updated')
    search_fields = ('flightnumb',)
