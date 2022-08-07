from django.db import models


class Auto(models.Model):
    owner = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=True, null=True)
    mark = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    count_of_passengers = models.IntegerField(blank=True, null=True, default=4)

    class Meta:
        managed = True
        db_table = 'cars'
        verbose_name = 'Car'


    def __str__(self):
        return f'{self.mark} {self.model}, {self.vehicle_number}'