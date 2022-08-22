from datetime import timedelta, datetime

from django.db import models


class Message(models.Model):
    time = models.DateTimeField(default=datetime.now)
    from_user = models.ForeignKey('users.Users', on_delete=models.CASCADE, related_name='user_from')
    to_user = models.ForeignKey('users.Users', on_delete=models.CASCADE, related_name='user_to')
    text = models.CharField(max_length=1000)

    class Meta:
        managed = True
        db_table = 'message'
