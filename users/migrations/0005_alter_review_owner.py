# Generated by Django 3.2.6 on 2022-08-07 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_review_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='users.users', verbose_name='Отправитель'),
        ),
    ]