# Generated by Django 4.2.7 on 2024-02-18 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branding', '0005_featuredbanner_sub_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuredbanner',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='herobrand',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]