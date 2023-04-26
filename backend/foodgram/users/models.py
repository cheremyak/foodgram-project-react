from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Админ'),
    ]
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Уникальный юзернейм',
        validators=[UnicodeUsernameValidator, validate_username]
    )
    first_name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        verbose_name='Фамилия'
    )
    subscribe = models.ManyToManyField(
        verbose_name='Подписка на других пользователей',
        related_name='subscriptions',
        to='self',
        symmetrical=False,
        blank=True
    )
    role = models.CharField(
        'Роль', max_length=9, choices=ROLES, default=USER,
        error_messages={'validators': 'Выбрана несуществующая роль'}
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def is_user(self):
        return self.role == self.USER

    def __str__(self):
        return self.username
