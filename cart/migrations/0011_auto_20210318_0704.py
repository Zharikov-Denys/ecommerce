# Generated by Django 3.1.6 on 2021-03-18 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_order_middle_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='completed',
            field=models.BooleanField(default=False, verbose_name='Завершена'),
        ),
    ]
