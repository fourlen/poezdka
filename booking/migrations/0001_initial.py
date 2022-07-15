# Generated by Django 3.2.6 on 2022-07-13 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0004_auto_20220704_2250'),
        ('trips', '0002_auto_20220703_0206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.trips')),
            ],
            options={
                'db_table': 'booking',
                'managed': True,
            },
        ),
    ]