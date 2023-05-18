# Generated by Django 3.2.18 on 2023-05-18 15:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=150, validators=[django.core.validators.RegexValidator(code='invalid_regex', message='При вводе имен/фамилий/названий рецептов допустимы только буквы кириллицы и латиницы. Проверьте введенные данные', regex='/^([а-яё]+|[a-z]+)$/i')], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150, validators=[django.core.validators.RegexValidator(code='invalid_regex', message='При вводе имен/фамилий/названий рецептов допустимы только буквы кириллицы и латиницы. Проверьте введенные данные', regex='/^([а-яё]+|[a-z]+)$/i')], verbose_name='Фамилия'),
        ),
    ]
