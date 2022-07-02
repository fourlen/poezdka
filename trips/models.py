from django.db import models


class Trips(models.Model):
    owner = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=True, null=True)
    car = models.ForeignKey('cars.Auto', on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    departure = models.CharField(max_length=100, blank=True, null=True)
    destination = models.CharField(max_length=100, blank=True, null=True)
    start = models.IntegerField(blank=True, null=True)
    end = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trips'


class TripsBooking(models.Model):
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=True, null=True)
    trip = models.ForeignKey('trips.Trips', on_delete=models.CASCADE, blank=True, null=True)
