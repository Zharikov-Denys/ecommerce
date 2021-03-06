# Generated by Django 3.1.6 on 2021-02-27 12:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Категория товара')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Название товара')),
                ('description', models.TextField(blank=True, verbose_name='Описание товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена на товар')),
                ('ratting', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                ('in_stock', models.BooleanField(default=True, verbose_name='В наличиии')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Обновлён')),
            ],
        ),
        migrations.CreateModel(
            name='ProductFeatures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_key', models.CharField(max_length=50, verbose_name='Ключ характеристики')),
            ],
        ),
        migrations.CreateModel(
            name='SpecificationValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=350, verbose_name='Значение характеристики')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Подкатегория товара')),
                ('slug', models.SlugField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория товара')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratting', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                ('review', models.TextField(verbose_name='Отзыв')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='mainapp.product', verbose_name='Продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.productfeatures', verbose_name='Ключ характеристики')),
                ('feature_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.specificationvalue', verbose_name='Значение характеристики')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='mainapp.product', verbose_name='Продукт')),
            ],
        ),
        migrations.CreateModel(
            name='ProductMeasurementsKeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement_key', models.CharField(max_length=50, verbose_name='Ключ измерения')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.subcategory', verbose_name='Подкатегория')),
            ],
        ),
        migrations.CreateModel(
            name='ProductMeasurements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.productmeasurementskeys', verbose_name='Ключ измерения')),
                ('measurement_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.specificationvalue', verbose_name='Значение измерения')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='mainapp.product', verbose_name='Продукт')),
            ],
        ),
        migrations.AddField(
            model_name='productfeatures',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.subcategory', verbose_name='Подкатегория'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.subcategory', verbose_name='Подкатегория товара'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images', verbose_name='Изображение товара')),
                ('image_url', models.URLField(blank=True, verbose_name='Ссылка на изображение товара')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product', verbose_name='Товар')),
            ],
        ),
    ]
