from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    email = models.EmailField(
        max_length=settings.EMAIL_MAX_CHARS,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    username = models.CharField(
        max_length=settings.USER_MAX_CHARS,
        unique=True,
        verbose_name='Уникальный юзернейм',
        validators=[
            UnicodeUsernameValidator(),
            validate_username
        ]
    )
    first_name = models.CharField(
        max_length=settings.USER_MAX_CHARS,
        blank=False,
        verbose_name='Имя',
        validators=[
            RegexValidator(
                '[A-zА-яЁё]',
                'Имя: допустимы только буквы кириллицы и латиницы'
            )
        ]
    )
    last_name = models.CharField(
        max_length=settings.USER_MAX_CHARS,
        blank=False,
        verbose_name='Фамилия',
        validators=[
            RegexValidator(
                '[A-zА-яЁё]',
                'Фамилия: допустимы только буквы кириллицы и латиницы'
            )
        ]
    )
    subscribe = models.ManyToManyField(
        verbose_name='Подписка на других пользователей',
        related_name='subscribers',
        to='self',
        symmetrical=False,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}: {self.email}'
