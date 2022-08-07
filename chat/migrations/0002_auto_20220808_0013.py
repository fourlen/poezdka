# Generated by Django 3.2.6 on 2022-08-07 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_users_options'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'managed': True},
        ),
        migrations.AddField(
            model_name='message',
            name='user_from',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_from', to='users.users'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='user_to',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_to', to='users.users'),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='message',
            table='message',
        ),
    ]