# Generated by Django 4.2.7 on 2024-01-26 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='street2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]