from django.db import models


class Trips(models.Model):
    owner = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=True, null=True)
    car = models.ForeignKey('cars.Auto', on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trips'


    # owner = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=True, null=True)
    # mark = models.CharField(max_length=100, blank=True, null=True)
    # model = models.CharField(max_length=100, blank=True, null=True)
    # color = models.CharField(max_length=100, blank=True, null=True)
    # vehicle_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    # count_of_passengers = models.IntegerField(blank=True, null=True)

    # class Meta:
    #     managed = True
    #     db_table = 'cars'
