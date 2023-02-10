# Generated by Django 4.1.3 on 2023-02-10 09:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuel', '0005_updatedatabase_alter_fuel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricetable',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(limit_value=1, message='Price must be greater then 0')]),
        ),
    ]