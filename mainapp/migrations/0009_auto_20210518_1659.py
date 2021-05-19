# Generated by Django 3.2 on 2021-05-18 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20210419_2326'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Изображение', 'verbose_name_plural': 'Изображения'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterModelOptions(
            name='productfeatures',
            options={'verbose_name': 'Ключ характеристики', 'verbose_name_plural': 'Ключи характеристик'},
        ),
        migrations.AlterModelOptions(
            name='productmeasurements',
            options={'verbose_name': 'Измерение товара', 'verbose_name_plural': 'Измерения товаров'},
        ),
        migrations.AlterModelOptions(
            name='productmeasurementskeys',
            options={'verbose_name': 'Ключ измерения', 'verbose_name_plural': 'Ключи измерений'},
        ),
        migrations.AlterModelOptions(
            name='productspecification',
            options={'verbose_name': 'Характеристика товара', 'verbose_name_plural': 'Характеристики товаров'},
        ),
        migrations.AlterModelOptions(
            name='returnitem',
            options={'verbose_name': 'Товар на возврат', 'verbose_name_plural': 'Товары на возврат'},
        ),
        migrations.AlterModelOptions(
            name='returnletter',
            options={'verbose_name': 'Заявление на возврат товара', 'verbose_name_plural': 'Заявления на возврат товаров'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-product__created_at', '-created_at'], 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterModelOptions(
            name='specificationvalue',
            options={'verbose_name': 'Значение характеристики', 'verbose_name_plural': 'Значения характеристик'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'Подкатегория', 'verbose_name_plural': 'Подкатегории'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='morga',
        ),
        migrations.AddField(
            model_name='product',
            name='markup',
            field=models.PositiveIntegerField(default=25, verbose_name='Наценка в %'),
        ),
        migrations.AlterField(
            model_name='product',
            name='true_price',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена на товар без наценки'),
        ),
    ]
