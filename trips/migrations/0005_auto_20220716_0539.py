# Generated by Django 3.2.6 on 2022-07-16 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220704_2250'),
        ('trips', '0004_auto_20220715_2349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stops',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lon', models.FloatField(blank=True, null=True)),
                ('district', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('population', models.IntegerField(blank=True, default=None, null=True)),
                ('subject', models.CharField(blank=True, max_length=100, null=True)),
                ('distance_to_previous', models.IntegerField(blank=True, null=True)),
                ('time', models.IntegerField(blank=True, null=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
            options={
                'db_table': 'stops',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='trips',
            name='end',
        ),
        migrations.AlterField(
            model_name='departure',
            name='district',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='departure',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='departure',
            name='lon',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='departure',
            name='population',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.DeleteModel(
            name='Destination',
        ),
    ]