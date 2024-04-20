# Generated by Django 4.2.7 on 2023-11-26 17:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('added_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Last Modified on')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='products/category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductSubCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('added_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Last Modified on')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='products/sub-category')),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productcategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('added_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Last Modified on')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='products/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productcategory')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productsubcategory')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]