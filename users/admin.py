from django.contrib import admin
from .models import Users

all_fields = ('login', 'first_name', 'last_name', 'gender', 'birth', 'photo')

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = all_fields
    search_fields = ['login', 'first_name', 'last_name']