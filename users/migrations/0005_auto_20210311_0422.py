# Generated by Django 3.1.6 on 2021-03-11 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210311_0312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, null=True, verbose_name='username'),
        ),
    ]
