import json

from django.db import models


class Booking(models.Model):
    owner = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=False, null=False,
                              verbose_name="Создатель")
    trip = models.ForeignKey('trips.Trips', on_delete=models.CASCADE, blank=False, null=False, verbose_name="Поездка")
    seat = models.CharField(max_length=500, blank=True, null=True, default="[0]", verbose_name="Место")

    def set_seat(self, x):
        self.seat = json.dumps(x)

    def get_seat(self):
        return [int(i) for i in self.seat[1:len(self.seat) - 1].split(', ')]

    class Meta:
        managed = True
        db_table = 'booking'
        verbose_name_plural = "Список броней"
