# Generated by Django 3.1.6 on 2021-03-12 05:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20210228_0047'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnLetter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('middle_name', models.CharField(max_length=255, verbose_name='Отчество')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('receive_order_date', models.DateField(verbose_name='Дата получения товара ')),
                ('order_number', models.CharField(max_length=50, verbose_name='№ заказа (или номер ТТН «Новой Почты»)')),
                ('bank_card_number', models.CharField(max_length=50, verbose_name='Номер банковской карты')),
                ('fml_card_owner', models.CharField(max_length=255, verbose_name='ФИО владельца карты')),
                ('completed', models.BooleanField(default=False, verbose_name='Возврат завершен')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReturnItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255, verbose_name='Название товара')),
                ('quantity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество товара')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Общая стоимость товара')),
                ('return_reason', models.CharField(choices=[('1', 'Не подошел по размеру.'), ('2', 'Не подошел по внешнему виду.'), ('3', 'Товар не соответствует заказу.'), ('4', 'Брак.'), ('5', 'Другая причина (пожалуйста, укажите, какая именно)')], max_length=1, verbose_name='Код причины возвращения')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('return_letter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='mainapp.returnletter', verbose_name='Заявление на возврат товара')),
            ],
        ),
    ]
