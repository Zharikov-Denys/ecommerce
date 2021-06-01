# Generated by Django 3.2 on 2021-05-28 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_product_price_before_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sales_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество продаж'),
        ),
    ]