# Generated by Django 3.2.6 on 2022-08-05 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='conditioner',
            field=models.BooleanField(default=False),
        ),
    ]
