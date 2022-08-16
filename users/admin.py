from django.contrib import admin
from .models import Users, Review

all_fields = ('login', 'id', 'is_active', 'first_name', 'last_name', 'gender', 'birth', 'photo', 'token')


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = all_fields
    search_fields = ['login', 'first_name', 'last_name']


@admin.register(Review)
class UsersReview(admin.ModelAdmin):
    list_display = ('owner', 'user', 'message', 'mark', 'date')
    search_fields = ['user']
