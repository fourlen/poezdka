from django.contrib import admin
from .models import *

all_fields = ('login', 'id', 'email', 'phone_number', 'is_active', 'first_name', 'last_name', 'photo', 'code', 'token', 'fcm_token')


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = all_fields
    search_fields = ['login', 'first_name', 'last_name']


@admin.register(Review)
class UsersReview(admin.ModelAdmin):
    list_display = ('id', 'owner', 'user', 'message', 'mark', 'date')
    search_fields = ['user']


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer')
    search_fields = ['question']


@admin.register(Blog)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'header', 'text')
    search_fields = ['header']
