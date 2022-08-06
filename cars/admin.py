from django.contrib import admin
from .models import Auto

all_fields = ('owner', 'mark', 'model', 'color', 'vehicle_number', 'count_of_passengers')

@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_display = all_fields