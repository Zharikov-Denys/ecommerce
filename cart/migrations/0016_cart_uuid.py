# Generated by Django 3.2 on 2021-05-26 13:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0015_alter_order_ttn'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]
