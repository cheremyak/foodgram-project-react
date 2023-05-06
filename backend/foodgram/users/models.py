from django.conf import settings
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
        max_length=settings.EMAIL_MAX_CHARS,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    username = models.CharField(
        max_length=settings.USER_MAX_CHARS,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Уникальный юзернейм',
        validators=[UnicodeUsernameValidator, validate_username]
    )
    first_name = models.CharField(
        max_length=settings.USER_MAX_CHARS,
        blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=settings.USER_MAX_CHARS,
        blank=False,
        verbose_name='Фамилия'
    )
    role = models.CharField(
        'Роль',
        max_length=settings.ROLE_MAX_LENGTH,
        choices=ROLES,
        default=USER,
        error_messages={'validators': 'Выбрана несуществующая роль'}
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == self.USER

    def __str__(self):
        return f'{self.username}: {self.email}'


class Follow(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='follower',
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='following'
    )

    class Meta:
        ordering = ('-id', )
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='no_self_follow'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f'{self.user} подписан на {self.author}'
