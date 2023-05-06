# Generated by Django 3.2.18 on 2023-05-06 10:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230503_0851'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscribe',
            field=models.ManyToManyField(blank=True, related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Подписка на других пользователей'),
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]