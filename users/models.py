from django.db import models


class Users(models.Model):
    login = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=500, blank=True, null=True)
    token = models.CharField(max_length=500, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=500, blank=True, null=True)
    last_name = models.CharField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    birth = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users'
