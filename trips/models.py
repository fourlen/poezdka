from django.db import models


class Trips(models.Model):
    owner = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Создатель')
    car = models.ForeignKey('cars.Auto', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Автомобиль')
    price = models.IntegerField(blank=True, null=True, verbose_name='Стоимость')
    start = models.IntegerField(blank=True, null=True, verbose_name='Время отъезда')
    package = models.BooleanField(blank=True, default=False, verbose_name='Посылка')
    baggage = models.BooleanField(blank=True, default=False, verbose_name='Багаж')
    baby_chair = models.BooleanField(blank=True, default=False, verbose_name='Детское кресло')
    smoke = models.BooleanField(blank=True, default=False, verbose_name='Можно курить')
    animals = models.BooleanField(blank=True, default=False, verbose_name='Можно с животными')
    two_places_in_behind = models.BooleanField(blank=True, default=False, verbose_name='2 места сзади')
    conditioner = models.BooleanField(blank=True, default=False, verbose_name='Кондиционер')
    premium = models.BooleanField(blank=True, default=False, verbose_name='Премиум')

    class Meta:
        managed = True
        db_table = 'trips'
        verbose_name_plural = 'Поездки'

    def __str__(self):
        return f'Поездка №{self.id}'


class Departure(models.Model):
    trip = models.ForeignKey('trips.Trips', on_delete=models.CASCADE, blank=False, null=False)
    lat = models.FloatField(blank=True, null=True, verbose_name='Широта')
    lon = models.FloatField(blank=True, null=True, verbose_name='Долгота')
    district = models.CharField(max_length=100, blank=True, null=True, default=None, verbose_name='Федеральный округ')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    population = models.IntegerField(blank=True, null=True, default=None, verbose_name='Население')
    subject = models.CharField(max_length=100, blank=True, null=True, verbose_name='Регион')

    class Meta:
        managed = True
        db_table = 'departures'
        verbose_name_plural = 'Пункты отправления'


class Stops(models.Model):
    trip = models.ForeignKey('trips.Trips', on_delete=models.CASCADE, blank=False, null=False)
    lat = models.FloatField(blank=True, null=True, verbose_name='Широта')
    lon = models.FloatField(blank=True, null=True, verbose_name='Долгота')
    district = models.CharField(max_length=100, blank=True, null=True, default=None, verbose_name='Федеральный округ')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    population = models.IntegerField(blank=True, null=True, default=None, verbose_name='Население')
    subject = models.CharField(max_length=100, blank=True, null=True, verbose_name='Регион')
    distance_to_previous = models.IntegerField(blank=True, null=True, verbose_name='Расстояние до пред. пункта в '
                                                                                   'поездке')
    time = models.IntegerField(blank=True, null=True, verbose_name='Время прибытия (timestamp)')

    class Meta:
        managed = True
        db_table = 'stops'
        verbose_name_plural = 'Остановки'
