from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'trip', 'seat')
    list_display_link = ('id', 'owner', 'trip')
