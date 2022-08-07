from django.db import models


class Message(models.Model):
    user_from = models.ForeignKey('users.Users', on_delete=models.CASCADE, related_name='user_from')
    user_to = models.ForeignKey('users.Users', on_delete=models.CASCADE, related_name='user_to')
    text = models.CharField(max_length=1000)

    class Meta:
        managed = True
        db_table = 'message'
