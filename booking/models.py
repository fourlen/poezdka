import json

from django.db import models


class Booking(models.Model):
    owner = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=False, null=False)
    trip = models.ForeignKey('trips.Trips', on_delete=models.CASCADE, blank=False, null=False)
    seat = models.CharField(max_length=500, blank=True, null=True, default="[1]")

    def set_seat(self, x):
        print(x)
        self.seat = json.dumps(x)

    def get_seat(self):
        return [int(i) for i in self.seat[1:len(self.seat) - 1].split(', ')]

    class Meta:
        managed = True
        db_table = 'booking'


class BannedUsers(models.Model):
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=False, null=False)
    trip = models.ForeignKey('trips.Trips', on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'banned_users'
        verbose_name = 'Banned user'
