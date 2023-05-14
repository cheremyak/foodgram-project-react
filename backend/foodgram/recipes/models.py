from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models.functions import Length

User = get_user_model()

models.CharField.register_lookup(Length)


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=settings.RECIPES_MAX_CHARS,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=settings.RECIPES_MAX_CHARS,
    )

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name', )
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_for_ingredient'
            ),
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name is empty\n',
            ),
            models.CheckConstraint(
                check=models.Q(measurement_unit__length__gt=0),
                name='\n%(app_label)s_%(class)s_measurement_unit is empty\n',
            ),
        )


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тэг',
        max_length=settings.RECIPES_MAX_CHARS,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=settings.HEX_MAX_CHARS,
        null=True,
        default='#',
        unique=True,
        validators=[
            RegexValidator(
                '^#(?:[0-9a-fA-F]{2}){3,4}$',
                'введите HEX-код цвета'
            )
        ]
    )
    slug = models.CharField(
        verbose_name='Слаг тэга',
        max_length=settings.TAG_SLUG_MAX_CHARS,
        unique=True,
    )

    def __str__(self):
        return f'{self.name} (цвет: {self.color})'

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name', )


class Recipe(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    tags = models.ManyToManyField(
        to=Tag,
        related_name='tags',
        verbose_name='Тэги'
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='',
    )
    name = models.CharField(
        max_length=settings.RECIPE_NAME_MAX_CHARS,
        verbose_name='Название рецепта'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                settings.MIN_COOKING_TIME_AMOUNT,
                'Время приготовления должно быть >=1 минуты'
            )
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False,
    )
    cart = models.ManyToManyField(
        to=User,
        verbose_name='Список покупок',
        related_name='carts',
    )

    def __str__(self):
        return f'{self.name}. Автор: {self.author.username}'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_for_author',
            ),
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name is empty\n',
            ),
        )


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        verbose_name='В рецептах',
        related_name='ingredient_amount',
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(
        to=Ingredient,
        verbose_name='Связанные ингредиенты',
        related_name='+',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0,
        validators=[
            MinValueValidator(
                settings.MIN_COOKING_TIME_AMOUNT,
                'Минимальное значение 1'
            )
        ]
    )

    def __str__(self):
        return f'{self.ingredients} {self.amount}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('recipe', )
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredients', ),
                name='\n%(app_label)s_%(class)s Ингредиент уже добавлен\n',
            ),
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепты'
    )

    class Meta():
        ordering = ('-id',)
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return 'Избранные рецепты'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    cart = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Список покупок'
    )

    class Meta():
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'cart'),
                name='unique_shopping_cart'
            )
        ]
