# Generated by Django 3.2.6 on 2022-07-02 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_delete_auto'),
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trips',
            name='end',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trips',
            name='start',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='TripsBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trips.trips')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
        ),
    ]