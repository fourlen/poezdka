from django.contrib import admin
from .models import Trips, Departure, Stops

all_fields = ('id', 'owner', 'car', 'price', 'start', 'package', 'baggage', 'baby_chair', 'smoke', 'animals', 'two_places_in_behind', 'conditioner', 'premium')


@admin.register(Trips)
class AutoTrips(admin.ModelAdmin):
    list_display = all_fields
    list_display_links = ('id', )


@admin.register(Departure)
class DepartureTrips(admin.ModelAdmin):
    list_display = ('id', 'trip', 'lat', 'lon', 'district', 'name', 'population', 'subject')
    list_display_links = ('id', 'trip')


@admin.register(Stops)
class StopsTrips(admin.ModelAdmin):
    list_display = ('id', 'trip', 'lat', 'lon', 'district', 'name', 'population', 'subject', 'distance_to_previous', 'time')
    list_display_links = ('id', 'trip')
