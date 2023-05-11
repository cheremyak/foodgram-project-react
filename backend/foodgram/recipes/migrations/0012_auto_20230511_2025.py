# Generated by Django 3.2.18 on 2023-05-11 17:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='amount',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1, 'Минимальное значение 1')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(default='#', max_length=7, null=True, unique=True, validators=[django.core.validators.RegexValidator('^[0-9A-F]+$', 'введите HEX-код цвета')], verbose_name='Цветовой HEX-код'),
        ),
    ]
