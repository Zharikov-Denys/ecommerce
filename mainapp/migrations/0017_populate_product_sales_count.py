# Generated by Django 3.2 on 2021-05-28 15:19

from django.db import migrations

def populate_product_sales_count(apps, schema_editor):
    Product = apps.get_model('mainapp', 'Product')
    Order = apps.get_model('cart', 'Order')
    for order in Order.objects.filter(status='completed'):
        for cart_item in order.cart.items.all():
            product = Product.objects.get(id=cart_item.product.id)
            product.sales_count += cart_item.quantity
            product.save()

class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_product_sales_count'),
    ]

    operations = [
        # omit reverse_code=... if you don't want the migration to be reversible.
        migrations.RunPython(populate_product_sales_count, reverse_code=migrations.RunPython.noop),
    ]