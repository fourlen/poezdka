from django.db import models


class Trips(models.Model):
    owner = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=True, null=True)
    car = models.ForeignKey('cars.Auto', on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    start = models.IntegerField(blank=True, null=True)
    package = models.BooleanField(blank=True, default=False)
    baggage = models.BooleanField(blank=True, default=False)
    baby_chair = models.BooleanField(blank=True, default=False)
    smoke = models.BooleanField(blank=True, default=False)
    animals = models.BooleanField(blank=True, default=False)
    two_places_in_behind = models.BooleanField(blank=True, default=False)
    conditioner = models.BooleanField(blank=True, default=False)
    premium = models.BooleanField(blank=True, default=False)

    class Meta:
        managed = True
        db_table = 'trips'
        verbose_name = 'Trip'


    def __str__(self):
        return f'Trip #{self.id}'

class Departure(models.Model):
    trip = models.ForeignKey('trips.Trips', on_delete=models.CASCADE, blank=False, null=False)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True, default=None)
    name = models.CharField(max_length=100, blank=True, null=True)
    population = models.IntegerField(blank=True, null=True, default=None)
    subject = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'departures'


class Stops(models.Model):
    trip = models.ForeignKey('trips.Trips', on_delete=models.CASCADE, blank=False, null=False)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True, default=None)
    name = models.CharField(max_length=100, blank=True, null=True)
    population = models.IntegerField(blank=True, null=True, default=None)
    subject = models.CharField(max_length=100, blank=True, null=True)
    distance_to_previous = models.IntegerField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stops'
        verbose_name = 'Stop'
