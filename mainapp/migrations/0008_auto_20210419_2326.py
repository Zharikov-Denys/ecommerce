# Generated by Django 3.2 on 2021-04-19 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20210320_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='first_name',
            field=models.CharField(default='Den', max_length=255, verbose_name='Имя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='second_name',
            field=models.CharField(default='Zharikov', max_length=255, verbose_name='Фамилия'),
            preserve_default=False,
        ),
    ]
