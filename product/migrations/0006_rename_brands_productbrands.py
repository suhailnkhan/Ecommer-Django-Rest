# Generated by Django 4.2.7 on 2024-01-09 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_brands_product_brand'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Brands',
            new_name='ProductBrands',
        ),
    ]