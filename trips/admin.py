from datetime import datetime

from django.contrib import admin
from .models import Trips, Departure, Stops

all_fields = ('id', 'owner', 'car', 'price', 'time_start', 'package', 'baggage', 'baby_chair', 'smoke', 'animals',
              'two_places_in_behind', 'conditioner', 'premium')


@admin.register(Trips)
class AutoTrips(admin.ModelAdmin):
    list_display = all_fields
    list_display_links = ('id', )

    def time_start(self, obj: Trips):
        return datetime.fromtimestamp(obj.start // 10**6)

    time_start.short_description = "Время отъезда"


@admin.register(Departure)
class DepartureTrips(admin.ModelAdmin):
    list_display = ('id', 'trip', 'lat', 'lon', 'district', 'name', 'population', 'subject')
    list_display_links = ('id', )


@admin.register(Stops)
class StopsTrips(admin.ModelAdmin):
    list_display = ('id', 'trip', 'lat', 'lon', 'district', 'name', 'population', 'subject', 'distance_to_previous', 'timer')
    list_display_links = ('id', )

    def timer(self, obj: Stops):
        return datetime.fromtimestamp(obj.time // 10**6)

    timer.short_description = "Время приезда"
