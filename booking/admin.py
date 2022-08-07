from django.contrib import admin
from .models import Booking, BannedUsers


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'trip', 'seat')
    list_display_link = ('id', 'owner', 'trip')


@admin.register(BannedUsers)
class BannedUsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'trip')
    list_display_link = ('id', 'user', 'trip')
