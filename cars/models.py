from django.db import models


class Auto(models.Model):
    owner = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Владелец')
    mark = models.CharField(max_length=100, blank=True, null=True, verbose_name='Марка')
    model = models.CharField(max_length=100, blank=True, null=True, verbose_name='Модель')
    color = models.CharField(max_length=100, blank=True, null=True, verbose_name='Цвет')
    vehicle_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Автомобильный номер')
    count_of_passengers = models.IntegerField(blank=True, null=True, default=4,
                                              verbose_name='Максимальное число пассажиров')

    class Meta:
        managed = True
        db_table = 'cars'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f'{self.mark} {self.model}, {self.vehicle_number}'
