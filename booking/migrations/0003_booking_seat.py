# Generated by Django 3.2.6 on 2022-08-06 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_bannedusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='seat',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
