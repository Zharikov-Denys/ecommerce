# Generated by Django 3.1.6 on 2021-03-18 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_auto_20210318_0518'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='middle_name',
            field=models.CharField(default='ИСегреевич', max_length=100, verbose_name='Отчество'),
            preserve_default=False,
        ),
    ]