from django.db import models


class Users(models.Model):
    login = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=500, blank=True, null=True)
    token = models.CharField(max_length=500, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=500, blank=True, null=True)
    last_name = models.CharField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    birth = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(null=True, blank=True, upload_to="media/")
    is_blocked = models.BooleanField(blank=True, default=False)

    class Meta:
        managed = True
        db_table = 'users'
        verbose_name = 'User'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Review(models.Model):
    owner = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=True, null=True, related_name="owner")
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=10000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'reviews'
