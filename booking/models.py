from django.db import models


class Booking(models.Model):
    owner = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=False, null=False)
    trip = models.ForeignKey('trips.Trips', on_delete=models.CASCADE, blank=False, null=False)
    seat = models.IntegerField(blank=True, null=True, default=1)

    class Meta:
        managed = True
        db_table = 'booking'


class BannedUsers(models.Model):
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=False, null=False)
    trip = models.ForeignKey('trips.Trips', on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'banned_users'
