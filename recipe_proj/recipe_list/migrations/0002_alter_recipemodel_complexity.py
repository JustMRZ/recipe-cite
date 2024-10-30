# Generated by Django 5.1 on 2024-09-02 09:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_list', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipemodel',
            name='complexity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
