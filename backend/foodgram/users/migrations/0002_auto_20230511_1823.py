# Generated by Django 3.2.18 on 2023-05-11 15:23

from django.conf import settings
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=150, validators=[django.core.validators.RegexValidator('A-zА-яЁё', 'Имя: допустимы только буквы кириллицы и латиницы')], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150, validators=[django.core.validators.RegexValidator('A-zА-яЁё', 'Фамилия: допустимы только буквы кириллицы и латиницы')], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='subscribe',
            field=models.ManyToManyField(blank=True, related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Подписка на других пользователей'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator(), users.validators.validate_username], verbose_name='Уникальный юзернейм'),
        ),
    ]
